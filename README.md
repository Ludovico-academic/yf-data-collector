# yf-data-collector

A small Python project for downloading market data from Yahoo Finance, transforming prices into returns, and exporting the results to Excel.

The project is designed for teaching purposes and shows a simple structured workflow:

- collect the data
- transform the data
- export the output

## Project structure

```text
yf-data-collector/
├── main.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── collect.py
│   ├── transform.py
│   └── export.py
└── data/
```

## Setup

Create and activate a virtual environment:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
```

Install the required packages:

```fish
pip install -r requirements.txt
```

## Run the project

```fish
python main.py
```

The output Excel file will be saved in:

```text
data/processed/yf_market_data.xlsx
```

## Workflow

1. Check the ticker on Yahoo Finance.
2. Add the ticker to `main.py`.
3. Download historical price data.
4. Extract closing prices.
5. Convert prices into simple returns.
6. Calculate cumulative returns.
7. Export the results to Excel.

## Notes

With `auto_adjust=True`, Yahoo Finance prices are adjusted for corporate actions such as dividends and stock splits. This makes the price series more suitable for return calculations.
