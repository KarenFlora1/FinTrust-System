import os
import sqlite3

TRANSFERS_DB = os.path.join(os.path.dirname(__file__), "transfers.db")

def add_transfer(transacion_id: str, from_account_id: int, to_account_id: int, amount: float):
    conn = sqlite3.connect(TRANSFERS_DB)
    cursor = conn.cursor()
    sql = """INSERT INTO transfers (transaction_id, from_account_id, to_account_id, amount) VALUES
    (:transaction_id, :from_account_id, :to_account_id, :amount)"""
    try:
        cursor.execute(sql, {
            "transaction_id": transacion_id,
            "from_account_id": from_account_id,
            "to_account_id": to_account_id, 
            "amount": amount
        })
    except sqlite3.OperationalError as e:
        conn.rollback()
        print(f"Error: creating `transfers` table: {e.with_traceback(None)}")
    conn.commit()
    conn.close()
    

def transfers(count: int = None):
    conn = sqlite3.connect(TRANSFERS_DB)
    cursor = conn.cursor()
    sql = "SELECT transaction_id, from_account_id, to_account_id, amount, time FROM transfers"
    if count is None:
        result = cursor.execute(sql).fetchall()
    else:
        result = cursor.execute(sql).fetchmany(count)
    conn.close()
    return [{
            "transactions_id": item[0],
            "from_account_id": item[1],
            "to_account_id": item[2],
            "amount": item[3],
            "time": item[4]} for item in result]

def account_transfers(account_id: int):
    conn = sqlite3.connect(TRANSFERS_DB)
    cursor = conn.cursor()
    sql = """SELECT transaction_id, from_account_id, to_account_id, amount, time FROM transfers 
            WHERE from_account_id = :account_id OR to_account_id = :account_id"""
    result = cursor.execute(sql, {"account_id": account_id}).fetchall()
    
    conn.close()
    return [{
            "transactions_id": item[0],
            "from_account_id": item[1],
            "to_account_id": item[2],
            "amount": item[3],
            "time": item[4]} for item in result]

def delete_transfer(transaction_id: int):
    conn = sqlite3.connect(TRANSFERS_DB)
    cursor = conn.cursor()
    sql = "DELETE from transfers where transaction_id = :transaction_id"
    cursor.execute(sql, {"transaction_id": transaction_id})
    conn.commit()
    conn.close()

if __name__ == '__main__':
    transaction_id1 = "dfsadsadassadsa897eqeqweqweqw7ewqneewqq_1" 
    transaction_id2 = "dfsadsadassadsa897eqeqweqweqw7ewqneewqq_2" 
    transaction_id3 = "dfsadsadassadsa897eqeqweqweqw7ewqneewqq_3" 
    delete_transfer(transaction_id=transaction_id1)
    delete_transfer(transaction_id=transaction_id2)
    delete_transfer(transaction_id=transaction_id3)
    print(transfers())
    add_transfer(transaction_id1, 1, 2, 1000.0)
    add_transfer(transaction_id2, 2, 1, 1000.0)
    add_transfer(transaction_id3, 2, 3, 1000.0)
    print(transfers(), end="\n\n")
    print(account_transfers(1),end="\n\n")
    delete_transfer(transaction_id=transaction_id1)
    delete_transfer(transaction_id=transaction_id2)
    delete_transfer(transaction_id=transaction_id3)
    print(transfers())