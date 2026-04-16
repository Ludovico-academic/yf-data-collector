from pathlib import Path

from src.collect import download_market_data, extract_close_prices
from src.transform import (
    calculate_simple_returns,
    calculate_cumulative_returns,
    resample_prices,
)
from src.export import export_to_excel


def run_market_data_pipeline(
    tickers: list[str],
    start_date: str,
    end_date: str,
    frequency: str,
    output_file: Path,
) -> None:
    market_data = download_market_data(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        frequency=frequency,
    )

    prices = extract_close_prices(market_data, tickers)
    prices = resample_prices(prices, frequency)

    returns = calculate_simple_returns(prices)
    cumulative_returns = calculate_cumulative_returns(returns)

    export_to_excel(
        prices=prices,
        returns=returns,
        cumulative_returns=cumulative_returns,
        file_path=output_file,
    )

    print(f"Done. Frequency: {frequency}")
    print(f"File saved to: {output_file}")