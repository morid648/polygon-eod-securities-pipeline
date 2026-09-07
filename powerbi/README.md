# `powerbi/`

## Purpose
Power BI deliverables built on top of the Snowflake `SA` (Subject Area)
analytical views — the business-facing output of the pipeline.

## Contents
| File | Purpose |
|------|---------|
| `securities_market_insights.pbix` | Original Power BI report file |
| `securities_market_insights.pdf` | Full report exported as PDF, for viewing without Power BI installed |
| `market_liquidity_overview.jpg` | Screenshot: sector liquidity contribution, traded value, ETF liquidity trends and ranking |
| `equity_watchlist_insights.jpg` | Screenshot: daily returns, OHLC pricing, top equities by volume, watchlist performance |

## Data Source
Both dashboards consume the `SA` schema views defined in
`snowflake/sec_pricing_views.sql` — not the raw fact/dimension tables
directly — so Power BI logic stays thin and the business rules live in SQL.

## How to Open
- **`.pbix`**: open in Power BI Desktop. You'll need a live Snowflake
  connection configured with your own credentials to refresh the data model;
  the file ships with the report layout and visuals, not embedded data.
- **`.pdf`**: static snapshot, opens in any PDF viewer — no Power BI or
  Snowflake connection required.
