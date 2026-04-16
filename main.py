from pathlib import Path
from src.pipeline import run_market_data_pipeline


TICKERS = ["AAPL", "MSFT", "^FTSE"]
START_DATE = "2023-01-01"
END_DATE = "2025-12-31"
FREQUENCY = "daily" # Choose: "daily", "monthly", "quarterly", or "yearly"
OUTPUT_FILE = Path(f"data/yf_market_data_{FREQUENCY}.xlsx")


def main() -> None:
    run_market_data_pipeline(
        tickers=TICKERS,
        start_date=START_DATE,
        end_date=END_DATE,
        frequency=FREQUENCY,
        output_file=OUTPUT_FILE,
    )


if __name__ == "__main__":
    main()
    