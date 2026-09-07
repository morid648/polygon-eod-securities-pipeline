# Data Quality & Validation

## Purpose
Validation controls run at multiple stages of the pipeline to prevent invalid
or incomplete data from silently reaching the analytical layer.

## Validation Stages

```
File Validation
      ↓
RAW Load Validation
      ↓
Pre-Merge Metrics
      ↓
CORE Data Quality
      ↓
Post-Merge Reconciliation
```

## 1. Local File Validation
Before S3 upload, `t02_verify_local_file` checks whether the expected CSV
exists at `/tmp/eod_<trading_date>.csv`. If not, it raises
`AirflowFailException` and the pipeline halts before upload.

## 2. RAW Load Validation
`sql/02_check_loaded.sql` confirms at least one record exists in
`RAW.RAW_EOD_PRICES` for the target trading date.

## 3. Negative Volume Validation
Rows with `VOLUME < 0` are treated as invalid and stored in
`CORE.EOD_PRICES_REJECT` with `REJECT_REASON = 'NEGATIVE_VOLUME'`, retaining
source/ingestion metadata.

## 4. Symbol Normalization
```sql
UPPER(TRIM(SYMBOL))
```
Reduces matching inconsistencies from casing or whitespace.

## 5. Duplicate Handling
CORE merge uses deterministic ordering by `_INGEST_TS` (latest wins), then
`_SRC_FILE`, to resolve duplicate `(SYMBOL, TRADE_DATE)` records.

## 6. Pre-Merge Metrics
| Metric | Meaning |
|--------|---------|
| RAW count | Records in RAW for the trading date |
| Reject count | Records with negative volume |
| Estimated inserts | Valid keys not already in CORE |
| Estimated updates | Valid keys already present in CORE |

## 7. Post-Merge Metrics
| Metric | Meaning |
|--------|---------|
| CORE rows | CORE records for the trading date |
| FACT rows | FACT records for the trading date |

Both feed into the Slack EOD summary.

## Data Quality Limitations
Not implemented in this pipeline:
- Null-price validation
- Price-relationship checks (e.g. `HIGH >= LOW`)
- Volume reconciliation against an external benchmark
- Statistical outlier detection
- Completeness checks against an expected security universe

These should not be represented as implemented controls without additional
code.
