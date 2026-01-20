import os
import sqlite3
AUTH_DB = os.path.join(os.path.dirname(__file__), "auth.db")

conn = sqlite3.connect(AUTH_DB)
cursor = conn.cursor()

if __name__ == '__main__':
    users_create_sql = """
    CREATE TABLE IF NOT EXISTS users(
        id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )"""
    
    active_users_create_sql = """
    CREATE TABLE IF NOT EXISTS  active_users(
        user_id TEXT NOT NULL,
        token  TEXT NOT NULL
    )"""

    clean_12_ids_sql = "DELETE FROM users WHERE id IN ('user1', 'user2', 'Karen', 'Manu');"

    initial_users_insert = """
    INSERT INTO users (id, username, password) values 
        ('user1', 'user1', 'pass1'),
        ('user2', 'user2', 'pass2'),
        ('Karen', 'Karen', '12345'),
        ('Manu', 'Manu', '12345');
    """

    try:
        cursor.execute(users_create_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: creating `users` table: {e.with_traceback(None)}")

    try:
        cursor.execute(active_users_create_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: creating `active_user` table: {e.with_traceback(None)}")

    try:
        cursor.execute(clean_12_ids_sql)
    except sqlite3.OperationalError as e:
        print(f"Error: deleting ids in `(user1, user2)` table: {e.with_traceback(None)}")

    try:
        cursor.execute(initial_users_insert)
    except sqlite3.OperationalError as e:
        print(f"inserting new users (user1, user2): {e.with_traceback(None)}")

    # Dangerous part of this migration it will clean up the databases
    conn.commit()
    conn.close()