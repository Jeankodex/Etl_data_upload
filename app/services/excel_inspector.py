import pandas as pd
from app.config.sheet_config import SHEET_CONFIG

def normalize_column(col_name):
    """Normalize column names: lowercase, replace spaces/special chars with underscore"""
    col_name = col_name.strip().lower().replace(" ", "_")
    col_name = ''.join(c for c in col_name if c.isalnum() or c == "_")
    return col_name

def inspect_excel(file_path):
    print("\n--- EXCEL INSPECTION STARTED ---")
    print(f"Excel file path: {file_path}\n")
    
    xls = pd.ExcelFile(file_path)
    sheets = xls.sheet_names
    print("Sheets found in Excel file:")
    for sheet in sheets:
        print(f"- {sheet}")
        
        if sheet not in SHEET_CONFIG:
            print(f"  ⚠ WARNING: Sheet '{sheet}' not configured. Skipping.")
            continue

        config = SHEET_CONFIG[sheet]
        header_row = config["header_row"] - 1  # convert 1-based to 0-based
        unique_key = config["unique_key"].lower()

        # Read only header row
        df_header = pd.read_excel(file_path, sheet_name=sheet, header=header_row, nrows=0)
        columns = [normalize_column(c) for c in df_header.columns]
        
        if unique_key not in columns:
            print(f"  ❌ ERROR: Unique key '{unique_key}' not found in columns for sheet '{sheet}'")
        else:
            print(f"  ✅ Columns extracted: {columns}")
            print(f"  ✅ Unique key '{unique_key}' verified")
    
    print("\n--- EXCEL INSPECTION COMPLETED ---\n")
