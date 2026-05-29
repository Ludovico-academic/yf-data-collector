"""
export.py — Save DataFrames to Excel.

Supports appending: if the output file already exists (e.g. because another
notebook already wrote to it), new sheets are added without deleting the
existing ones. If a sheet with the same name already exists, it is replaced.
"""

from pathlib import Path
import pandas as pd


def save_to_excel(sheets: dict[str, pd.DataFrame], file_path: Path) -> None:
    """
    Write one or more DataFrames to an Excel file, each on its own sheet.

    Parameters
    ----------
    sheets    : dict mapping sheet name → DataFrame
    file_path : path to the output .xlsx file

    Behaviour
    ---------
    - If the file does not exist, it is created.
    - If the file already exists (from a previous notebook run), new sheets are
      added and existing sheets with the same name are updated in place.
      All other sheets in the file are left untouched.
    - Empty DataFrames are skipped.
    """
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Filter out empty DataFrames
    non_empty = {
        name: df for name, df in sheets.items()
        if df is not None and not df.empty
    }

    if not non_empty:
        raise ValueError("All DataFrames are empty — nothing to save.")

    mode = "a" if file_path.exists() else "w"
    extra = {"if_sheet_exists": "replace"} if mode == "a" else {}

    with pd.ExcelWriter(file_path, engine="openpyxl", mode=mode, **extra) as writer:
        for sheet_name, df in non_empty.items():
            # Sheet names in Excel are limited to 31 characters
            safe_name = sheet_name[:31]
            df.to_excel(writer, sheet_name=safe_name)
