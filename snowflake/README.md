# `snowflake/`

## Purpose
One-time Snowflake setup scripts: warehouse/database/schema creation, table
DDL, the S3 storage integration, the reject table, and the analytical (SA)
views consumed by Power BI. Run these once to provision the environment that
`sql/` and `historical_load/` then operate against.

## Contents
| File | Purpose |
|------|---------|
| `init_snowflake_objects.sql` | Creates the warehouse, database, all four schemas (`RAW`, `CORE`, `DM_DIM`, `DM_FACT`), and the RAW/CORE/dimension/fact table DDL |
| `load_daily_eod_prices.sql` | Defines the CSV file format, S3 storage integration, and external stage used by `sql/01_copy_to_raw.sql` |
| `reject_table.sql` | Creates `CORE.EOD_PRICES_REJECT` for negative-volume and other rejected records |
| `sec_pricing_views.sql` | Creates the `SA` schema, `DIM_SECURITY_ATTRIBUTES` table, and six business-ready analytical views consumed by Power BI |

## Run Order

```
1. init_snowflake_objects.sql     (warehouse, database, schemas, core tables)
2. reject_table.sql               (reject table)
3. load_daily_eod_prices.sql      (file format, storage integration, stage)
4. sec_pricing_views.sql          (SA schema + analytical views)
```

After this, the Airflow DAG (`dags/`) and/or `historical_load/` can populate
and maintain the tables.

## Analytical Views (`sec_pricing_views.sql`)
| View | Purpose |
|------|---------|
| `VW_SECURITY_DAILY_PRICES` | Business-ready daily OHLCV joined with security attributes |
| `VW_TOP20_EQUITY_BY_VOLUME_DAILY` | Daily top-20 equities by volume and traded value |
| `VW_WATCHLIST_HISTORY` | Historical pricing/liquidity for a fixed 10-symbol watchlist |
| `VW_SECURITY_LAST_30D_DAILY_RETURN` | Last 30 days of daily % returns per equity |
| `VW_SECTOR_LIQUIDITY_LATEST` | Latest-day sector liquidity and % contribution |
| `VW_ETF_LIQUIDITY_30D_SUMMARY` | 30-day ETF liquidity averages and ranking |

## Before Running
- Replace `<YOUR_AWS_ACCOUNT_ID>` and `<YOUR_S3_BUCKET>` in
  `load_daily_eod_prices.sql` with your own AWS account ID and bucket name.
- The storage integration step also requires creating an IAM role
  (`snowflake_s3_integration_role`) in AWS first, with a trust relationship
  to Snowflake's external ID — see Snowflake's storage integration docs.
- `DIM_SECURITY_ATTRIBUTES` (symbol → name/sector/industry/type) is created
  empty by `sec_pricing_views.sql`; it needs to be populated separately
  (e.g. from a reference data source) before the views return sector/industry
  detail.
