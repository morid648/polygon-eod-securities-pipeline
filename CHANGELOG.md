# Changelog

All notable changes to this project are documented in this file.

## [1.1.0] - 2026-09-07

### Added
- Snowflake DDL and setup scripts (`snowflake/`): warehouse/database/schema
  creation, RAW/CORE/dimension/fact table definitions, S3 storage
  integration, external stage, reject table, and six Subject Area (SA)
  analytical views
- Historical backfill path (`historical_load/`): standalone Polygon
  extraction script plus a matching RAW → CORE → Dimensions → FACT
  transform, independent of the daily Airflow DAG
- Power BI deliverables (`powerbi/`): `.pbix` report, PDF export, and two
  dashboard screenshots (market liquidity overview, equity/watchlist
  insights)
- Architecture and data-model diagrams (`docs/architecture.png`,
  `docs/data_model.png`, `docs/daily_eod_data_pipeline.png`)
- Standalone connection-verification DAGs for AWS, Slack, and Snowflake
  (`docs/test_scripts/`)
- `docker-compose.yaml` and `.env.example` for local Airflow setup
- READMEs for all new folders (`historical_load/`, `snowflake/`, `powerbi/`,
  `docs/test_scripts/`)

### Changed
- Root README rewritten to cover the full platform (historical + daily
  pipelines, Snowflake data model, analytics layer, Power BI, setup steps)
- SQL filenames in `sql/` renamed to a zero-padded convention
  (`01_copy_to_raw.sql` … `08_postmerge_metrics.sql`)
- Main DAG file renamed to `dags/polygon_eod_pipeline_dag.py`
- Test-script filenames renamed for clarity (`test_aws_connection.py`, etc.)

### Security
- Replaced a hardcoded AWS account ID and S3 bucket name in
  `snowflake/load_daily_eod_prices.sql` with placeholders
- Replaced a hardcoded S3 bucket name in
  `docs/test_scripts/test_aws_connection.py` with a placeholder

## [1.0.0] - 2026-09-07

### Added
- Initial published version of the pipeline under this account
- Airflow DAG (`polygon_eod_data_downloader_final_v2`) with 5-stage task
  sequence: download → verify → upload → Snowflake load → Slack summary
- `lib/eod_data_downloader.py` — Polygon grouped-daily extraction with
  lookback-based trading-day resolution
- `lib/slack_utils.py` — Slack Incoming Webhook helper and Airflow
  failure callback
- 8-step Snowflake SQL pipeline (`sql/01_copy_to_raw.sql` through
  `sql/08_postmerge_metrics.sql`) covering RAW → CORE → Dimensions → FACT →
  post-merge audit
- Documentation: root README, per-folder READMEs, `docs/data_flow.md`,
  `docs/data_quality.md`

