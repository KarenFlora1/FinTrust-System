import os
import sqlite3

TRANSFERS_DB = os.path.join(os.path.dirname(__file__), "transfers.db")
if __name__ == '__main__':
    conn = sqlite3.connect(TRANSFERS_DB)
    cursor = conn.cursor()

    transfers_create_sql = """
    CREATE TABLE IF NOT EXISTS transfers(
        transaction_id TEXT PRIMARY KEY,
        from_account_id INTEGER NOT NULL,
        to_account_id INTEGER NOT NULL,
        amount DECIMAL(15, 2) NOT NULL,
        time DATETIME DEFAULT CURRENT_TIMESTAMP
    );"""

    try:
        cursor.execute(transfers_create_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: creating `transfers` table: {e.with_traceback(None)}")
    conn.commit()
    conn.close()