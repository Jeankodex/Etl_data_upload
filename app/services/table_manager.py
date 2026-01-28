
from app.services.db import get_connection

SYSTEM_COLUMNS = [
    "created_at TEXT DEFAULT CURRENT_TIMESTAMP",
    "updated_at TEXT DEFAULT CURRENT_TIMESTAMP"
]

def create_table(sheet_name: str, columns: list, unique_key: str):
    """
    Create a table for a sheet with normalized columns and system columns.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Build column definitions
    col_defs = [f"{col} TEXT" for col in columns]  # all columns TEXT for simplicity
    col_defs.extend(SYSTEM_COLUMNS)

    # Add unique constraint
    col_defs.append(f"UNIQUE({unique_key})")

    table_name = sheet_name.lower().replace(" ", "_")
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        {', '.join(col_defs)}
    );
    """

    cursor.execute(sql)
    conn.commit()
    conn.close()

    print(f"✅ Table '{table_name}' created or already exists.")
