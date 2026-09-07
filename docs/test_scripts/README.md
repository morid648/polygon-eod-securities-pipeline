# `docs/test_scripts/`

## Purpose
Standalone, minimal Airflow DAGs used to verify each external connection
independently before relying on them inside the main pipeline. Useful for
first-time setup and for isolating connection issues from pipeline logic
issues.

## Contents
| File | DAG ID | Verifies |
|------|--------|----------|
| `test_aws_connection.py` | `test_aws_conn` | `aws_default` — lists objects from an S3 bucket |
| `test_slack_connection.py` | `test_slack_conn` | `slack_default` — posts a test message via the Incoming Webhook |
| `test_snowflake_connection.py` | `test_snowflake_conn` | `snowflake_default` — runs a `SELECT CURRENT_USER()...` context check |

## How to Run
1. Copy the desired script into your Airflow `dags/` folder
2. In `test_aws_connection.py`, replace `"your-s3-bucket-name"` with a bucket
   your `aws_default` connection actually has access to
3. Trigger the DAG manually from the Airflow UI (all three have
   `schedule=None`, so they only run on demand)
4. Check the task logs for a success message, or the exception raised on
   failure

## Notes
These are diagnostic tools, not part of the production DAG — they're not
wired into `dags/polygon_eod_pipeline_dag.py` and can be safely removed from
an Airflow deployment once connections are confirmed working.
