from pathlib import Path
import pandas as pd


def export_to_excel(prices: pd.DataFrame, returns: pd.DataFrame, cumulative_returns: pd.DataFrame, file_path: Path) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        prices.to_excel(writer, sheet_name="Prices")
        returns.to_excel(writer, sheet_name="Returns")
        cumulative_returns.to_excel(writer, sheet_name="Cumulative Returns")
