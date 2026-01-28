
import pandas as pd
from app.services.db import get_connection
from app.config.sheet_config import SHEET_CONFIG

def normalize_column(col_name):
    """Normalize column names the same way as in inspection"""
    col_name = col_name.strip().lower().replace(" ", "_")
    col_name = ''.join(c for c in col_name if c.isalnum() or c == "_")
    return col_name

def insert_sheet_data(file_path: str):
    """Insert Excel data into SQLite tables sheet by sheet"""
    conn = get_connection()
    cursor = conn.cursor()

    for sheet_name, config in SHEET_CONFIG.items():
        data_start_row = config["data_start_row"] - 1  # convert 1-based to 0-based
        unique_key = config["unique_key"].lower()

        # Read sheet data starting from the data_start_row
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=data_start_row - 1)
        df.columns = [normalize_column(c) for c in df.columns]

        table_name = sheet_name.lower().replace(" ", "_")
        inserted = 0
        skipped = 0

        for _, row in df.iterrows():
            values = tuple(row[col] if col in row else None for col in df.columns)

            placeholders = ", ".join("?" for _ in df.columns)
            columns_str = ", ".join(df.columns)

            # Use INSERT OR IGNORE to prevent duplicate unique key insertion
            sql = f"""
                INSERT OR IGNORE INTO {table_name} ({columns_str})
                VALUES ({placeholders});
            """
            cursor.execute(sql, values)

            if cursor.rowcount:
                inserted += 1
            else:
                skipped += 1

        conn.commit()
        print(f"Sheet '{sheet_name}' → inserted: {inserted}, skipped (duplicates): {skipped}")

    conn.close()
