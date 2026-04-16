import pandas as pd


def resample_prices(
    prices: pd.DataFrame,
    frequency: str,
) -> pd.DataFrame:
    """
    Resample prices when needed.

    Daily, monthly, and quarterly data are downloaded directly from Yahoo Finance.
    Yearly data is created from monthly data using the last available price each year.
    """

    if frequency == "yearly":
        prices = prices.resample("YE").last()

    return prices


def calculate_simple_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Convert prices into simple returns.
    """

    returns = prices.pct_change(fill_method=None)
    returns = returns.dropna(how="all")

    return returns


def calculate_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Convert simple returns into cumulative returns.
    """

    cumulative_returns = (1 + returns).cumprod() - 1

    return cumulative_returns