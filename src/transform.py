"""
transform.py — Functions to resample and transform price series.
"""

import pandas as pd


def resample_prices(prices: pd.DataFrame, frequency: str) -> pd.DataFrame:
    """
    Resample a daily or monthly price series to the requested frequency.

    Yahoo Finance does not offer yearly intervals directly, so yearly data
    is downloaded as monthly and resampled here to the last trading day
    of each calendar year.

    Parameters
    ----------
    prices    : DataFrame of close prices (dates as index)
    frequency : "Daily", "Monthly", "Quarterly", or "Yearly"
    """
    if frequency == "Yearly":
        prices = prices.resample("YE").last()
    return prices


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate simple (percentage) period returns from a price series.

    Return for period t = (Price_t - Price_{t-1}) / Price_{t-1}
    The first row is dropped because there is no previous price to compare.
    """
    returns = prices.pct_change(fill_method=None)
    returns = returns.dropna(how="all")
    return returns


def calculate_cumulative_returns(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate cumulative returns from a simple returns series.

    Cumulative return at date t = (1 + r_1) × (1 + r_2) × … × (1 + r_t) − 1

    A value of 0.25 means a 25% total gain since the start of the series.
    """
    cumulative = (1 + returns).cumprod() - 1
    return cumulative
