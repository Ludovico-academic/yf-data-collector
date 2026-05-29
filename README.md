# yf-data-collector

A set of Jupyter notebooks for downloading financial data from Yahoo Finance.
Designed for students with little or no Python experience.

---

## What's included

```
yf-data-collector/
├── notebooks/
│   ├── 01_stocks.ipynb      ← Stock-level data (prices, ratios, ESG, statements…)
│   ├── 02_indexes.ipynb     ← Stock market indexes
│   └── 03_macro.ipynb       ← Macro data (rates, commodities, FX, crypto)
├── viz/
│   └── visualisation.ipynb  ← Charts and correlation analysis
├── src/
│   ├── collect.py           ← Data collection functions
│   ├── transform.py         ← Return calculations
│   └── export.py            ← Excel export
├── data/                    ← Output folder (Excel files saved here)
├── requirements.txt
└── README.md
```

---

## Setup — step by step

Follow these steps **once** when you first set up the project.

### 1. Install Python

If you do not have Python installed, download it from [python.org](https://www.python.org/downloads/).  
Install version **3.11 or newer**. Make sure to tick **"Add Python to PATH"** during installation.

To check your Python version, open a terminal and run:
```
python --version
```

### 2. Download the project

Download the project folder and unzip it somewhere you can find it,
for example your Desktop or Documents folder.

### 3. Open a terminal in the project folder

**macOS / Linux**
1. Open Terminal
2. Type `cd ` (with a space after it), then drag the project folder into the terminal window
3. Press Enter

**Windows**
1. Open File Explorer and navigate to the project folder
2. Click on the address bar, type `cmd`, and press Enter

You should now see the project folder path in your terminal prompt.

### 4. Create a virtual environment

A virtual environment keeps this project's packages separate from the rest of your system.

```bash
python -m venv .venv
```

### 5. Activate the virtual environment

**macOS / Linux (bash/zsh):**
```bash
source .venv/bin/activate
```

**macOS (fish shell):**
```bash
source .venv/bin/activate.fish
```

**Windows:**
```
.venv\Scripts\activate
```

You will see `(.venv)` appear at the start of your terminal prompt. This means the environment is active.

> ⚠️ You need to activate the environment **every time** you open a new terminal window.

### 6. Install the required packages

```bash
pip install -r requirements.txt
```

This may take a minute or two.

### 7. Launch JupyterLab

```bash
jupyter lab
```

A browser window will open automatically. If it does not, look for a URL in the terminal output that starts with `http://localhost:8888/` and open it manually.

---

## How to use the notebooks

### Notebooks in `notebooks/`

Open **01_stocks.ipynb**, **02_indexes.ipynb**, or **03_macro.ipynb** depending on what data you need.

Each notebook follows the same four-step workflow:
1. Run the Setup cell
2. Enter tickers / select series
3. Set the date range and frequency
4. Click **Download Data**

The output Excel file is saved in the `data/` folder.

**Combining data across notebooks**  
If you use the same file name (e.g. `market_data.xlsx`) in more than one notebook,
each notebook adds its own sheets to that file without overwriting the others.
You end up with a single Excel file containing all your data on separate sheets.

### Visualisation notebook (`viz/visualisation.ipynb`)

Open this notebook after you have downloaded some data.  
It reads your Excel file and produces:
- Price / level evolution chart
- Return distribution histograms
- Correlation heatmap

---

## How to cite Yahoo Finance data in your assignment

After each download, the notebook prints a ready-to-use citation block:

```
Source     : Yahoo Finance (finance.yahoo.com)
Tickers    : AAPL, MSFT, GOOGL
Period     : 2020-01-01 to 2024-12-31  |  Frequency: Monthly
Downloaded : 15 January 2025
Tool       : yfinance Python library (pypi.org/project/yfinance)
```

Copy this text directly into the data section of your assignment.

---

## Troubleshooting

**`No price data returned`**  
Double-check the ticker on [finance.yahoo.com](https://finance.yahoo.com). Some tickers are exchange-specific (e.g. `MC.PA` for LVMH on Euronext Paris).

**`ESG data not available`**  
ESG scores are not available for all companies. This is normal for smaller firms and non-US stocks.

**Financial statements are empty**  
Indexes and ETFs do not have financial statements. Use financial statements only for individual company stocks.

**Widgets do not appear / look broken**  
Make sure JupyterLab is up to date. Run `pip install --upgrade jupyterlab ipywidgets` and restart.

**`ModuleNotFoundError`**  
Make sure the virtual environment is activated (you should see `(.venv)` in the terminal) and that you ran `pip install -r requirements.txt`.
