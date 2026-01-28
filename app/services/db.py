
import sqlite3
from sqlite3 import Connection
import os

DB_FILE = os.path.join(os.path.dirname(__file__), "../../data/etl_data.db")

def get_connection() -> Connection:
    """Create or return a SQLite connection."""
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # optional: return rows as dict-like
    return conn
