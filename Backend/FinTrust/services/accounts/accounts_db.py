import sqlite3
import os

ACCOUNTS_DB = os.path.join(os.path.dirname(__file__), "accounts.db")

def accounts(count: int = None):
    conn = sqlite3.connect(ACCOUNTS_DB)
    cursor = conn.cursor()
    sql = "SELECT id, user_id, balance FROM accounts"
    if count is None:
        result = cursor.execute(sql).fetchall()
    else:
        result = cursor.execute(sql).fetchmany(count)
    conn.close()
    return [{"account_id": item[0], "user_id": item[1], "balance": item[2]} for item in result]

def list_transfers_by_accounts(account_id: int):
    return get_account_by_id(account_id)


def user_accounts(user_id: str):
    conn = sqlite3.connect(ACCOUNTS_DB)
    cursor = conn.cursor()
    sql = "SELECT id, user_id, balance FROM accounts WHERE user_id = :user_id"
    result = cursor.execute(sql, {"user_id": user_id}).fetchall()
    conn.close()
    return [{"account_id": item[0], "user_id": item[1], "balance": item[2]} for item in result]

def user_account(user_id: str, account_id: int):
    conn = sqlite3.connect(ACCOUNTS_DB)
    cursor = conn.cursor()
    sql = "SELECT id, user_id, balance FROM accounts WHERE user_id = :user_id AND id = :id"
    result = cursor.execute(sql, {"user_id": user_id, "id": account_id}).fetchone()
    conn.close()
    return {"account_id": result[0], "user_id": result[1], "balance": result[2]}

def get_account_by_id(id: int):
    conn = sqlite3.connect(ACCOUNTS_DB)
    cursor = conn.cursor()
    sql = "SELECT id, user_id, balance FROM accounts WHERE id = :id"
    result = cursor.execute(sql, {"id": id}).fetchone()
    conn.close()
    return {"account_id": result[0], "user_id": result[1], "balance": result[2]}

def update_balance(id: int, balance: float):
    conn = sqlite3.connect(ACCOUNTS_DB)
    cursor = conn.cursor()
    sql = "UPDATE accounts set balance = :balance WHERE id = :id"
    try:
        cursor.execute(sql, {"id": id, "balance": balance})
    except sqlite3.OperationalError as e:
        conn.rollback()
        print(f"Error: updating ballace for account with id {id}: {e.with_traceback(None)}")
    conn.commit()
    conn.close()

if __name__ == '__main__':
    print(accounts())
    print(get_account_by_id(1))
    print(user_accounts('user1'))
    print(user_account('user1', 1))
    update_balance(1, 100.0)
    print(user_account('user1', 1))
    update_balance(1, 1000.0)