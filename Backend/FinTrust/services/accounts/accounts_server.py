import os
import threading
from concurrent import futures
from datetime import datetime

import grpc
import accounts_pb2
import accounts_pb2_grpc
import accounts_db

# Mock mantido (não é usado pelo ListAccounts)
accounts_data = {
    1: {"user_id": "user1", "balance": 1000.0},
    2: {"user_id": "user1", "balance": 500.0},
    3: {"user_id": "user2", "balance": 750.0}
}
data_lock = threading.Lock()


def _normalize_user_id(uid) -> str:
    """Aceita '1' -> 'user1', '2' -> 'user2', e mantém 'user1'/'user2'."""
    s = str(uid or "").strip()
    if s.isdigit():
        return f"user{s}"
    return s


class AccountsServer(accounts_pb2_grpc.AccountsServiceServicer):
    def ListAccounts(self, request: accounts_pb2.UserRequest, context) -> accounts_pb2.AccountsResponse:
        user_id = _normalize_user_id(getattr(request, "user_id", ""))
        rows = accounts_db.user_accounts(user_id=user_id)

        resp = accounts_pb2.AccountsResponse()
        for acc in rows:
            a = resp.accounts.add()
            a.id = int(acc["account_id"])
            a.user_id = str(acc["user_id"])
            a.balance = float(acc["balance"])
        return resp

    def UpdateBalance(self, request: accounts_pb2.UpdateBalanceRequest, context) -> accounts_pb2.UpdateBalanceResponse:
        acc_id = int(getattr(request, "account_id", 0))
        amount = float(getattr(request, "amount", 0.0))

        with data_lock:
            account = accounts_db.get_account_by_id(acc_id)
            if not account:
                r = accounts_pb2.UpdateBalanceResponse()
                r.success = False
                r.new_balance = 0.0
                r.message = "account not found"
                r.user_id = ""
                return r

            current_balance = float(account["balance"])
            if amount < 0 and current_balance < -amount:
                r = accounts_pb2.UpdateBalanceResponse()
                r.success = False
                r.new_balance = current_balance
                r.message = "insufficient balance"
                r.user_id = str(account["user_id"])
                return r

            new_balance = current_balance + amount
            accounts_db.update_balance(acc_id, new_balance)

            r = accounts_pb2.UpdateBalanceResponse()
            r.success = True
            r.new_balance = new_balance
            r.message = "balance updated successfully"
            r.user_id = str(account["user_id"])
            return r


def serve():
    ACCOUNT_SERVER_PORT = int(os.getenv("ACCOUNTS_PORT", "50052"))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    accounts_pb2_grpc.add_AccountsServiceServicer_to_server(AccountsServer(), server)
    # Bind para toda a rede (necessário para acesso a partir de outra máquina)
    server.add_insecure_port(f"0.0.0.0:{ACCOUNT_SERVER_PORT}")
    server.start()
    now = datetime.now()
    print(f"{now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} Running account server on port {ACCOUNT_SERVER_PORT}")

    import signal
    def handle_signal(*_):
        n = datetime.now()
        print(f"{n.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} Stopping account server...")
        server.stop(grace=5)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
