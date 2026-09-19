import sys
from pathlib import Path
from dotenv import load_dotenv
import os
import datetime as dt
import time
import csv

# Allow importing lib/ from this sibling directory when run as a standalone script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from lib.eod_data_downloader import get_stock_prices

load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")
SLEEP_SECONDS = 12


def extract_historical_data():
    start_date = dt.date(2026, 8, 1)
    end_date = dt.date(2026, 8, 11)

    out_file = (
        f"polygon_eod_grouped_"
        f"{start_date.strftime('%Y%m%d')}_"
        f"{end_date.strftime('%Y%m%d')}.csv"
    )
    # Static metadata for all rows in this file
    ingest_ts = (
        dt.datetime.now(dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
    )

    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trade_date", "symbol", "open", "high", "low", "close", "volume", "_src_file", "_ingest_ts"])

        current_date = start_date
        while current_date <= end_date:
            print(f"Fetching {current_date} ...")
            results = get_stock_prices(current_date, API_KEY)
            if results:
                print(f"{current_date}: {len(results)} rows")
                for row in results:
                    writer.writerow([
                        current_date,
                        row.get("T", ""),
                        row.get("o", ""),
                        row.get("h", ""),
                        row.get("l", ""),
                        row.get("c", ""),
                        row.get("v", ""),
                        out_file,
                        ingest_ts
                    ])
                    f.flush()  # Force write to disk immediately
            else:
                print(f"No results for {current_date}, It is weekend or holiday.")

            current_date += dt.timedelta(days=1)
            time.sleep(SLEEP_SECONDS)

    print(f"\n✅ Done! Saved: {out_file}")


if __name__ == "__main__":
    extract_historical_data()
