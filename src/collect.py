import pandas as pd
import yfinance as yf


def download_market_data(
    tickers: list[str],
    start_date: str,
    end_date: str,
    frequency: str = "daily",
) -> pd.DataFrame:
    """
    Download historical market data from Yahoo Finance.
    """

    interval_map = {
        "daily": "1d",
        "monthly": "1mo",
        "quarterly": "3mo",
        "yearly": "1mo",  # downloaded monthly, then resampled to year-end
    }

    if frequency not in interval_map:
        raise ValueError(
            "Invalid frequency. Choose: daily, monthly, quarterly, or yearly."
        )

    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        interval=interval_map[frequency],
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if data.empty:
        raise ValueError("No data downloaded. Check the ticker(s) and date range.")

    data.index.name = "Date"

    return data


def extract_close_prices(
    market_data: pd.DataFrame,
    tickers: list[str],
) -> pd.DataFrame:
    """
    Extract adjusted close prices.

    With auto_adjust=True, the Close column is adjusted for dividends and splits.
    """

    if isinstance(market_data.columns, pd.MultiIndex):
        prices = market_data["Close"].copy()
    else:
        prices = market_data[["Close"]].copy()
        prices.columns = tickers

    prices = prices.dropna(how="all")

    return prices