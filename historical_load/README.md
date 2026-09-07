# `historical_load/`

## Purpose
One-time / on-demand backfill path used to seed the warehouse with historical
EOD pricing data, independent of the daily Airflow DAG.

## Contents
| File | Purpose |
|------|---------|
| `extract_historical_data.py` | Pulls Polygon grouped-daily data across a date range and writes a single CSV with source/ingestion metadata |
| `load_transform_historical_data.sql` | Merges the historical CSV through CORE → Dimensions → FACT, mirroring the daily pipeline's transformation logic |

## How to Run

1. Set `POLYGON_API_KEY` in a local `.env` file (see `.env.example` at the repo root)
2. Edit the `start_date` / `end_date` range in `extract_historical_data.py`
3. Run the extraction script:
   ```bash
   python historical_load/extract_historical_data.py
   ```
   This writes a CSV named `polygon_eod_grouped_<start>_<end>.csv` to the
   working directory, rate-limited with a 12-second sleep between requests.
4. Stage the CSV into Snowflake RAW (e.g. via `PUT` + `COPY INTO`, using the
   file format and stage defined in `snowflake/load_daily_eod_prices.sql`)
5. Run `load_transform_historical_data.sql` in a Snowflake worksheet to merge
   RAW → CORE → Dimensions → FACT

## Notes
- This path does not go through Airflow or S3 — it's meant for backfilling
  history once, not for ongoing scheduled runs (that's what `dags/` is for).
- The transform SQL uses the same dedup and merge logic as the daily pipeline
  (`_INGEST_TS` + `_SRC_FILE` tie-breaking), so historical and daily loads
  stay consistent.
