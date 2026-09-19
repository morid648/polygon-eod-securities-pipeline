import csv
import requests
from airflow.exceptions import AirflowFailException
import logging
import pendulum

# Initialize logger for logging events
log = logging.getLogger(__name__)

POLYGON_BASE_URL = 'https://api.polygon.io'  # Base URL for Polygon API


def get_stock_prices(req_date, api_key):
    """
    Fetches the Polygon grouped-daily (EOD) results for a single trading date.

    Arguments:
    - req_date: date (or "YYYY-MM-DD" string) to fetch grouped-daily data for.
    - api_key: API key for authentication with the Polygon API.

    Returns a list of per-symbol result dicts, or [] if none are available.
    """
    url = f"{POLYGON_BASE_URL}/v2/aggs/grouped/locale/us/market/stocks/{req_date}"
    params = {"adjusted": "true", "include_otc": "false", "apiKey": api_key}

    try:
        r = requests.get(url, params=params, timeout=60)
        log.info("[polygon] %s -> %s", r.url, r.status_code)  # Log the request URL and response status
    except Exception as e:
        log.warning("[polygon] request failed for %s: %s", req_date, e)
        return []

    if r.status_code == 200 and r.json().get("resultsCount", 0) > 0:
        return r.json().get("results", [])
    return []


def download_polygon_eod_data_to_csv(POLYGON_API_KEY, LOOKBACK_DAYS):
    """
    Downloads the Polygon grouped daily (EOD) data and stores it as a CSV file.

    Arguments:
    - POLYGON_API_KEY: API key for authentication with the Polygon API.
    - LOOKBACK_DAYS: Number of days to look back to find the latest trading day with data.
    """

    # Ensure that the Polygon API Key is provided
    if not POLYGON_API_KEY:
        raise AirflowFailException("Missing Polygon API Key in Airflow Variables.")

    EXCHANGE_TZ = 'America/New_York'  # Timezone for trading day resolution
    today = pendulum.now(EXCHANGE_TZ).date()  # Get today's date in the specified exchange timezone

    # Iterate through the past 'POLYGON_MAX_LOOKBACK_DAYS' days to find a valid trading day
    for i in range(LOOKBACK_DAYS):
        # Calculate the target date by subtracting i days from today
        trading_date = today - pendulum.duration(days=i)
        trading_date = trading_date.strftime("%Y-%m-%d")  # Format the date as "YYYY-MM-DD"

        results = get_stock_prices(trading_date, POLYGON_API_KEY)

        # If the response is successful and contains results, write to CSV
        if results:
            log.info("Found valid trading data for date: %s", trading_date)

            # Define the CSV structure: (header name, Polygon result key)
            columns = [
                ("symbol", "T"),
                ("open", "o"),
                ("high", "h"),
                ("low", "l"),
                ("close", "c"),
                ("volume", "v"),
            ]

            # Write the data to the CSV file
            out_path = f"/tmp/eod_{trading_date}.csv"  # Define a fixed path for storing the CSV file locally
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow(["trade_date"] + [name for name, _ in columns])  # Write header row
                for row in results:
                    w.writerow([trading_date] + [row.get(key, "") for _, key in columns])  # Write the trading day data

            # Return the date for further use (if needed)
            return trading_date
        else:
            log.info("No data for date: %s, trying previous day.", trading_date)

    # If no valid trading day is found within the lookback window, raise an exception
    raise AirflowFailException("No grouped-daily data found within lookback window")
