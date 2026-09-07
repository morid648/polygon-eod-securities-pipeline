# `docs/`

## Purpose
Supporting documentation that goes deeper than the root README — intended for
anyone (recruiter, interviewer, collaborator) who wants to understand the
pipeline's design decisions in more detail.

## Contents
| File / Folder | Covers |
|------|--------|
| `data_flow.md` | End-to-end data flow, orchestration sequence, trading-date resolution, observability |
| `data_quality.md` | Validation stages, reject handling, deduplication logic, known limitations |
| `architecture.png` | System architecture diagram (Polygon → Airflow → S3 → Snowflake → Power BI) |
| `daily_eod_data_pipeline.png` | Diagram of the daily Airflow task sequence |
| `data_model.png` | Snowflake dimensional model diagram (RAW → CORE → DIM/FACT → SA) |
| `test_scripts/` | Standalone Airflow DAGs for verifying AWS, Slack, and Snowflake connections independently of the main pipeline |

## How to Use
Read `data_flow.md` first for the big picture, then `data_quality.md` for the
specific controls implemented at each stage. The three `.png` diagrams are
referenced directly in the root README.

Before running the main pipeline for the first time, use `test_scripts/` to
confirm each Airflow connection (`aws_default`, `slack_default`,
`snowflake_default`) is configured correctly — see
`test_scripts/README.md`.
