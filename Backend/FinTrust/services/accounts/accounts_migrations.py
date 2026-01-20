import os
import sqlite3


ACCOUNTS_DB = os.path.join(os.path.dirname(__file__), "accounts.db")
if __name__ == '__main__':
    conn = sqlite3.connect(ACCOUNTS_DB)
    cursor = conn.cursor()

    accounts_create_sql = """
    CREATE TABLE IF NOT EXISTS accounts(
        id INTEGER auto_increment,
        user_id TEXT NOT NULL,
        balance DECIMAL(15, 2) DEFAULT 0.0
    );"""

    delete_accounts_123_sql = """
    DELETE FROM accounts WHERE id IN (1, 2, 3, 4, 5);
    """


    add_initials_accounts_sql = """
    INSERT INTO accounts(id, user_id, balance) VALUES 
        (1, 'user1', 1000.0),
        (2, 'user1', 500.0),
        (3, 'user2', 756000.0),
        (4, 'Karen', 75000.0),
        (5, 'Manu', 750000.0);
    """

    try:
        cursor.execute(accounts_create_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: creating `accounts` table: {e.with_traceback(None)}")

    try:
        cursor.execute(delete_accounts_123_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: creating `accounts` table: {e.with_traceback(None)}")

    try:
        cursor.execute(add_initials_accounts_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: creating `accounts` table: {e.with_traceback(None)}")
    conn.commit()
    conn.close() 