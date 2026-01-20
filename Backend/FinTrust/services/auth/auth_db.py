# FinTrust/services/auth/auth_db.py
import sqlite3
import os

AUTH_DB = os.path.join(os.path.dirname(__file__), "auth.db")

def _conn():
    return sqlite3.connect(AUTH_DB)

def get_user(username: str, password: str):
    con = _conn(); cur = con.cursor()
    row = cur.execute(
        "SELECT id, username FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    con.close()
    if not row:
        return None
    return {"user_id": row[0], "username": row[1]}

def users(count: int = None):
    con = _conn(); cur = con.cursor()
    sql = "SELECT id, username FROM users"
    rows = cur.execute(sql).fetchall() if count is None else cur.execute(sql).fetchmany(count)
    con.close()
    return [{"user_id": r[0], "username": r[1]} for r in rows]

def _ensure_active_users(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS active_users(
            token   TEXT PRIMARY KEY,
            user_id TEXT
        )
    """)

def add_active_user(user_id: str, token: str):
    con = _conn(); cur = con.cursor()
    _ensure_active_users(cur)
    # substitui/actualiza se já existir token para o mesmo utilizador
    cur.execute("INSERT OR REPLACE INTO active_users(token, user_id) VALUES(?,?)", (token, user_id))
    con.commit(); con.close()

def get_active_user(token: str):
    con = _conn(); cur = con.cursor()
    _ensure_active_users(cur)
    row = cur.execute("SELECT user_id FROM active_users WHERE token=?", (token,)).fetchone()
    con.close()
    if not row:
        return None
    return {"user_id": row[0]}

def clear_active_users():
    con = _conn(); cur = con.cursor()
    _ensure_active_users(cur)
    cur.execute("DELETE FROM active_users")
    con.commit(); con.close()

if __name__ == '__main__':
    print(users(2))
