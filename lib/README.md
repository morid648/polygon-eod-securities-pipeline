# `lib/`

## Purpose
Reusable Python helper modules used by the Airflow DAG. Kept separate from
the DAG file so extraction logic and notification logic can be tested and
modified independently.

## Contents
| File | Purpose |
|------|---------|
| `eod_data_downloader.py` | Retrieves grouped daily market data from Polygon and writes it to CSV |
| `slack_utils.py` | Slack notification helper + Airflow task-failure callback |

## `eod_data_downloader.py`

```python
download_polygon_eod_data_to_csv(POLYGON_API_KEY, LOOKBACK_DAYS)
```

- Resolves "today" using the `America/New_York` timezone
- Walks backward day-by-day (up to `LOOKBACK_DAYS`) until Polygon's grouped
  daily endpoint returns results — handles weekends/holidays without
  hardcoding a market calendar
- Writes results to `/tmp/eod_<trading_date>.csv` with columns:
  `trade_date, symbol, open, high, low, close, volume`
- Raises `AirflowFailException` if no trading day with data is found in the
  lookback window, or if the API key is missing

## `slack_utils.py`

```python
_get_webhook_url()      # builds the webhook URL from the slack_default connection
slack_post(text)        # posts a message, returns True/False
on_task_failure(context)  # Airflow failure callback — posts DAG/task/run/error + log link
```

Uses the Airflow connection `slack_default` (Incoming Webhook). `on_task_failure`
is wired into the DAG's `on_failure_callback`, so any task failure produces a
Slack alert automatically — no extra code needed per task.

## How to Run / Test
These modules are plain Python and can be imported and unit tested outside
of Airflow, with the exception of `on_task_failure`, which expects an Airflow
task-instance context dict.

```python
from lib.eod_data_downloader import download_polygon_eod_data_to_csv
download_polygon_eod_data_to_csv("your_api_key", 10)
```
