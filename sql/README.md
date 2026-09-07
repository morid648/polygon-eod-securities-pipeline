# `sql/`

## Purpose
Snowflake SQL transformations executed by the `t04_snowflake_load` TaskGroup.
Implements the warehouse-processing portion of the pipeline:

```
S3 → RAW → Validation → CORE → Dimensions → FACT → Post-load Audit
```

## Contents
| File | Airflow Task ID | Stage | Purpose |
|------|------------------|-------|---------|
| `01_copy_to_raw.sql` | `s01_copy_to_raw` | RAW | Loads staged CSV into `RAW.RAW_EOD_PRICES` |
| `02_check_loaded.sql` | `s02_check_loaded_for_dt` | Validation | Confirms RAW has records for the trading date |
| `03_premerge_metrics.sql` | `s03_compute_premerge_metrics` | Validation | RAW count, reject count, estimated inserts/updates |
| `04_merge_core.sql` | `s04_merge_core_eod` | CORE | Rejects negative volume, dedupes, merges into CORE |
| `05_merge_dim_security.sql` | `s05_merge_dim_security` | Dimension | Inserts new symbols into `DM_DIM.DIM_SECURITY` |
| `06_merge_dim_date.sql` | `s06_merge_dim_date` | Dimension | Maintains `DM_DIM.DIM_DATE` |
| `07_merge_fact_daily_price.sql` | `s07_merge_fact_daily_price` | FACT | Merges into `DM_FACT.FACT_DAILY_PRICE` |
| `08_postmerge_metrics.sql` | `s08_compute_postmerge_metrics` | Validation | Compares CORE and FACT row counts |

## Execution Order (as wired in the DAG)
```
copy_to_raw → check_loaded → premerge_metrics → merge_core
                                                     │
                                    ┌────────────────┴────────────────┐
                                    ▼                                 ▼
                          merge_dim_security                merge_dim_date
                                    └────────────────┬────────────────┘
                                                      ▼
                                          merge_fact_daily_price
                                                      ▼
                                             postmerge_metrics
```

## Key Behaviors
- **Symbol normalization:** `UPPER(TRIM(SYMBOL))`
- **Negative-volume rejection:** rows with `VOLUME < 0` go to
  `CORE.EOD_PRICES_REJECT` with `REJECT_REASON = 'NEGATIVE_VOLUME'`
- **Deduplication:** deterministic ordering by `_INGEST_TS` (latest) then
  `_SRC_FILE`
- **Fact merge key:** `SECURITY_ID + DATE_SK`

## How to Run
These scripts are not meant to be run standalone in isolation — they're
invoked in sequence by `SQLExecuteQueryOperator` tasks in the DAG, using
Jinja params (`params.trading_ds_task_id`) to pull the resolved trading date
from XCom. To run manually in a Snowflake worksheet, replace the Jinja
template expressions with a literal date string first.

## Important Note
This repository does not include the Snowflake DDL for `RAW`, `CORE`,
`DM_DIM`, or `DM_FACT` schemas/tables. These scripts assume those objects
already exist.
