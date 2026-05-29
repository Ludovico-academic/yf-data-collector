"""
collect.py — Yahoo Finance data collection functions.

Each function downloads one type of data and returns a clean DataFrame.
Used by the three notebooks: stocks, indexes, and macro.
"""

import pandas as pd
import yfinance as yf


# ── Interval mapping ─────────────────────────────────────────────────────────

INTERVAL_MAP = {
    "Daily":     "1d",
    "Monthly":   "1mo",
    "Quarterly": "3mo",
    "Yearly":    "1mo",   # downloaded as monthly, then resampled to year-end
}


# ── 1. Price Data ─────────────────────────────────────────────────────────────

def download_prices(
    tickers: list[str],
    start: str,
    end: str,
    frequency: str,
) -> pd.DataFrame:
    """
    Download historical adjusted close prices from Yahoo Finance.

    Parameters
    ----------
    tickers   : list of ticker symbols, e.g. ["AAPL", "MSFT"]
    start     : start date string, e.g. "2020-01-01"
    end       : end date string,   e.g. "2025-12-31"
    frequency : one of "Daily", "Monthly", "Quarterly", "Yearly"

    Returns
    -------
    DataFrame — dates as rows, tickers as columns.
    Prices are adjusted for dividends and stock splits (auto_adjust=True).
    """
    interval = INTERVAL_MAP.get(frequency, "1mo")

    raw = yf.download(
        tickers=tickers,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )

    if raw.empty:
        raise ValueError(
            "No price data returned. Check tickers and date range."
        )

    # Extract Close — handles both single and multiple tickers
    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"].copy()
    else:
        prices = raw[["Close"]].copy()
        prices.columns = tickers

    prices.index.name = "Date"
    prices = prices.dropna(how="all")
    return prices


# ── 2. Company Info ───────────────────────────────────────────────────────────

_COMPANY_FIELDS = {
    "longName":            "Company Name",
    "sector":              "Sector",
    "industry":            "Industry",
    "country":             "Country",
    "currency":            "Currency",
    "exchange":            "Exchange",
    "fullTimeEmployees":   "Full-Time Employees",
    "marketCap":           "Market Cap",
    "enterpriseValue":     "Enterprise Value",
    "website":             "Website",
    "longBusinessSummary": "Business Description",
}

def get_company_info(tickers: list[str]) -> pd.DataFrame:
    """
    Retrieve company profile — sector, industry, market cap, etc.
    Returns one row per ticker.
    """
    rows = []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            row = {"Ticker": ticker}
            for key, label in _COMPANY_FIELDS.items():
                row[label] = info.get(key, None)
            rows.append(row)
        except Exception as e:
            rows.append({"Ticker": ticker, "Error": str(e)})

    return pd.DataFrame(rows).set_index("Ticker")


# ── 3. Valuation Ratios ───────────────────────────────────────────────────────

_VALUATION_FIELDS = {
    "trailingPE":                   "P/E (Trailing)",
    "forwardPE":                    "P/E (Forward)",
    "priceToBook":                  "Price-to-Book",
    "priceToSalesTrailing12Months": "Price-to-Sales",
    "enterpriseToEbitda":           "EV/EBITDA",
    "enterpriseToRevenue":          "EV/Revenue",
    "pegRatio":                     "PEG Ratio",
    "trailingEps":                  "EPS (Trailing)",
    "forwardEps":                   "EPS (Forward)",
    "bookValue":                    "Book Value per Share",
    "dividendYield":                "Dividend Yield",
    "payoutRatio":                  "Payout Ratio",
    "returnOnEquity":               "Return on Equity (ROE)",
    "returnOnAssets":               "Return on Assets (ROA)",
    "profitMargins":                "Net Profit Margin",
    "operatingMargins":             "Operating Margin",
    "grossMargins":                 "Gross Margin",
    "debtToEquity":                 "Debt-to-Equity",
    "currentRatio":                 "Current Ratio",
    "quickRatio":                   "Quick Ratio",
    "beta":                         "Beta",
    "52WeekChange":                 "52-Week Price Change",
    "sharesOutstanding":            "Shares Outstanding",
}

def get_valuation_ratios(tickers: list[str]) -> pd.DataFrame:
    """
    Retrieve current valuation and financial health ratios.
    Returns one row per ticker.

    Note: these are point-in-time (today's) figures, not historical series.
    """
    rows = []
    for ticker in tickers:
        try:
            info = yf.Ticker(ticker).info
            row = {"Ticker": ticker}
            for key, label in _VALUATION_FIELDS.items():
                row[label] = info.get(key, None)
            rows.append(row)
        except Exception as e:
            rows.append({"Ticker": ticker, "Error": str(e)})

    return pd.DataFrame(rows).set_index("Ticker")


# ── 4. Dividends ──────────────────────────────────────────────────────────────

def get_dividends(
    tickers: list[str],
    start: str,
    end: str,
) -> pd.DataFrame:
    """
    Retrieve dividend payment history within the selected date range.
    Returns a DataFrame with payment dates as rows and tickers as columns.
    """
    series = {}
    for ticker in tickers:
        try:
            divs = yf.Ticker(ticker).dividends
            if divs is not None and not divs.empty:
                divs.index = divs.index.tz_localize(None)
                mask = (
                    (divs.index >= pd.Timestamp(start)) &
                    (divs.index <= pd.Timestamp(end))
                )
                filtered = divs[mask]
                if not filtered.empty:
                    series[ticker] = filtered
        except Exception:
            pass

    if not series:
        return pd.DataFrame(columns=tickers)

    result = pd.DataFrame(series)
    result.index.name = "Payment Date"
    return result.dropna(how="all")


# ── 5. ESG Scores ─────────────────────────────────────────────────────────────

def get_esg_scores(tickers: list[str]) -> pd.DataFrame:
    """
    Retrieve ESG sustainability scores sourced from Sustainalytics via Yahoo Finance.

    Scores include: total ESG risk, environmental, social, governance sub-scores,
    and controversy level. Not all companies have ESG coverage.
    """
    rows = []
    for ticker in tickers:
        try:
            sust = yf.Ticker(ticker).sustainability
            if sust is not None and not sust.empty:
                row = {"Ticker": ticker}
                for metric in sust.index:
                    row[str(metric)] = sust.loc[metric].iloc[0]
                rows.append(row)
            else:
                rows.append({"Ticker": ticker, "Note": "ESG data not available"})
        except Exception as e:
            rows.append({"Ticker": ticker, "Error": str(e)})

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).set_index("Ticker")


# ── 6. Financial Statements ───────────────────────────────────────────────────

def get_financial_statement(
    tickers: list[str],
    statement: str,
    quarterly: bool = False,
) -> pd.DataFrame:
    """
    Retrieve financial statements for one or more tickers.

    Parameters
    ----------
    tickers   : list of ticker symbols
    statement : "income"   → Income Statement
                "balance"  → Balance Sheet
                "cashflow" → Cash Flow Statement
    quarterly : False = annual data (default), True = quarterly data

    Returns
    -------
    DataFrame with MultiIndex rows (Ticker, Line Item) and date columns.
    """
    dfs = {}
    for ticker in tickers:
        try:
            t = yf.Ticker(ticker)
            if statement == "income":
                df = t.quarterly_income_stmt if quarterly else t.income_stmt
            elif statement == "balance":
                df = t.quarterly_balance_sheet if quarterly else t.balance_sheet
            elif statement == "cashflow":
                df = t.quarterly_cashflow if quarterly else t.cashflow
            else:
                continue

            if df is not None and not df.empty:
                dfs[ticker] = df
        except Exception:
            pass

    if not dfs:
        return pd.DataFrame()

    combined = pd.concat(dfs, axis=0)
    combined.index.names = ["Ticker", "Line Item"]
    return combined
