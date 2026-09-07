# Data Flow

## End-to-End Flow

```
Polygon API
    │  grouped daily market data
    ▼
Python Downloader (lib/eod_data_downloader.py)
    │  CSV
    ▼
Local /tmp
    │  Airflow S3 transfer
    ▼
Amazon S3  (market/bronze/eod/)
    │  COPY INTO
    ▼
Snowflake RAW  (RAW.RAW_EOD_PRICES)
    │  validation + metrics
    ▼
Snowflake CORE  (CORE.EOD_PRICES)
    │
    ├──────────────┐
    ▼              ▼
DIM_SECURITY   DIM_DATE
    │              │
    └──────┬───────┘
           ▼
   FACT_DAILY_PRICE
           ▼
   Post-Merge Audit
           ▼
        Slack
```

## Airflow Orchestration

DAG: `polygon_eod_data_downloader_final_v2`

```
t01_download_to_csv
        ↓
t02_verify_local_file
        ↓
t03_upload_to_s3
        ↓
t04_snowflake_load   (TaskGroup, 8 SQL steps)
        ↓
t05_notify_slack_summary
```

## Trading Date Handling

The downloader resolves "today" using `America/New_York`, then searches
backward up to `LOOKBACK_DAYS` until Polygon's grouped daily endpoint returns
results. This avoids assuming that a calendar date is a trading day (handles
weekends/holidays without a hardcoded market calendar).

The resolved date is pushed to XCom under the key `trading_date` and pulled
by every downstream task, keeping the whole run pinned to one trading date.

## Data Quality Flow

Records with `VOLUME < 0` are identified during CORE processing and routed to
`CORE.EOD_PRICES_REJECT` with `REJECT_REASON = 'NEGATIVE_VOLUME'`. Valid
records continue through CORE → dimensions → FACT.

## Observability

**Pre-merge metrics:** RAW rows, reject rows, estimated inserts, estimated updates
**Post-merge metrics:** CORE rows, FACT rows

Both sets of metrics are pulled from XCom and included in the final Slack
summary message.

## Reliability Controls

```
retries = 3
retry_delay = 5 minutes
max_active_runs = 1
catchup = False
```

Task failures route through the DAG's `on_failure_callback`
(`lib/slack_utils.py:on_task_failure`), posting DAG, task, run ID, error
message, and a log link to Slack.
