# `dags/`

## Purpose
Contains the Airflow DAG definition that orchestrates the full pipeline —
from Polygon extraction through Snowflake loading to the Slack summary.

## Contents
| File | Purpose |
|------|---------|
| `polygon_eod_pipeline_dag.py` | Main DAG (`polygon_eod_data_downloader_final_v2`): task sequencing, retries, and the Snowflake TaskGroup |

## Task Sequence
```
t01_download_to_csv
      ↓
t02_verify_local_file
      ↓
t03_upload_to_s3
      ↓
t04_snowflake_load   (TaskGroup — see sql/README.md)
      ↓
t05_notify_slack_summary
```

## Configuration
- **DAG ID:** `polygon_eod_data_downloader_final_v2`
- **Schedule:** `5 21 * * 1-5` (weekdays, 21:05)
- **Retries:** 3, with a 5-minute delay
- **`max_active_runs`:** 1
- **`catchup`:** `False`
- **Failure callback:** `lib/slack_utils.py:on_task_failure`
- **`template_searchpath`:** points at `sql/`, so `SQLExecuteQueryOperator`
  tasks can reference SQL files by name

## How to Run
1. Set Airflow Variables: `POLYGON_API_KEY`, `LOOKBACK_DAYS`, `S3_BUCKET`
2. Configure connections: `aws_default`, `snowflake_default`, `slack_default`
3. Place this file (and the `lib/` and `sql/` folders) in your Airflow DAGs
   directory, preserving relative structure
4. Trigger manually from the Airflow UI, or wait for the scheduled run

## Notes
- The Slack summary task uses `trigger_rule="all_done"` so it fires even if
  an upstream task fails or is skipped — failures are still surfaced.
- Trading date resolution happens in `t01_download_to_csv` and is passed to
  every downstream task via XCom (`key="trading_date"`).
