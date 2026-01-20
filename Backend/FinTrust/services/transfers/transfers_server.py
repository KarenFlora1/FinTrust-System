import os
import sys
import uuid
from concurrent import futures
from datetime import datetime

import grpc
import transfers_pb2
import transfers_pb2_grpc

# DB local de transferências
import transfers_db

# Aceder ao serviço de contas (import dos stubs)
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'accounts'))
import accounts_pb2
import accounts_pb2_grpc

# ===== Config por variáveis de ambiente =====
ACCOUNTS_ADDR         = os.getenv("ACCOUNTS_ADDR", "127.0.0.1:50052")
TRANSFERS_SERVICE_PORT= int(os.getenv("TRANSFERS_PORT", "50053"))

# Canal para o serviço de contas (pode estar noutra máquina)
accounts_channel = grpc.insecure_channel(ACCOUNTS_ADDR)
accounts_stub = accounts_pb2_grpc.AccountsServiceStub(accounts_channel)


class TransferService(transfers_pb2_grpc.TransferServiceServicer):
    def MakeTransfer(self, request: transfers_pb2.TransferRequest, context) -> transfers_pb2.TransferResponse:
        from_acc = int(getattr(request, "from_account_id", 0))
        to_acc   = int(getattr(request, "to_account_id", 0))
        amount   = float(getattr(request, "amount", 0.0))

        if amount <= 0:
            return transfers_pb2.TransferResponse(success=False, transaction_id="", message="amount must be positive")
        if from_acc == to_acc:
            return transfers_pb2.TransferResponse(
                success=False, transaction_id="", message="destination account and origin account must be different"
            )

        # Debitar
        try:
            debit_resp = accounts_stub.UpdateBalance(
                accounts_pb2.UpdateBalanceRequest(account_id=from_acc, amount=-amount)
            )
        except Exception:
            return transfers_pb2.TransferResponse(
                success=False, transaction_id="", message="error while communicating with accounts service (debit)"
            )
        if not getattr(debit_resp, "success", False):
            return transfers_pb2.TransferResponse(
                success=False, transaction_id="", message=getattr(debit_resp, "message", "debit failed")
            )

        # Creditar (com rollback em caso de falha)
        try:
            credit_resp = accounts_stub.UpdateBalance(
                accounts_pb2.UpdateBalanceRequest(account_id=to_acc, amount=amount)
            )
        except Exception:
            try:
                accounts_stub.UpdateBalance(
                    accounts_pb2.UpdateBalanceRequest(account_id=from_acc, amount=amount)
                )
            finally:
                return transfers_pb2.TransferResponse(
                    success=False, transaction_id="", message="error while communicating with accounts service (credit)"
                )
        if not getattr(credit_resp, "success", False):
            try:
                accounts_stub.UpdateBalance(
                    accounts_pb2.UpdateBalanceRequest(account_id=from_acc, amount=amount)
                )
            finally:
                return transfers_pb2.TransferResponse(
                    success=False, transaction_id="", message=getattr(credit_resp, "message", "credit failed")
                )

        # Persistir no histórico (não quebra a operação em caso de falha)
        tx_id = str(uuid.uuid4())
        try:
            # compat com versões antigas
            transfers_db.add_transfer(
                transaction_id=tx_id,
                from_account_id=from_acc,
                to_account_id=to_acc,
                amount=amount,
            )
        except TypeError:
            # fallback para assinatura legacy (se o nome do parâmetro era 'transacion_id')
            try:
                transfers_db.add_transfer(
                    transacion_id=tx_id,
                    from_account_id=from_acc,
                    to_account_id=to_acc,
                    amount=amount,
                )
            except Exception:
                pass
        except Exception:
            pass

        msg = f"transfer of {amount:.2f} done successfully."
        return transfers_pb2.TransferResponse(success=True, transaction_id=tx_id, message=msg)

    def GetHistory(self, request: transfers_pb2.UserRequest, context) -> transfers_pb2.TransferHistoryResponse:
        """
        Busca contas do user no serviço de accounts e filtra o histórico local (transfers.db).
        """
        user_id = getattr(request, "user_id", "")
        try:
            accs_resp = accounts_stub.ListAccounts(accounts_pb2.UserRequest(user_id=user_id))
            account_ids = [acc.id for acc in accs_resp.accounts]
        except Exception:
            return transfers_pb2.TransferHistoryResponse(items=[])

        # Junta os registos de todas as contas do user
        rows = []
        for acc_id in account_ids:
            try:
                rows.extend(transfers_db.account_transfers(acc_id) or [])
            except Exception:
                continue

        items = []
        for r in rows:
            try:
                items.append(
                    transfers_pb2.TransferItem(
                        timestamp=str(r["timestamp"]),
                        from_account_id=int(r["from_account_id"]),
                        to_account_id=int(r["to_account_id"]),
                        amount=float(r["amount"]),
                    )
                )
            except Exception:
                continue

        return transfers_pb2.TransferHistoryResponse(items=items)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transfers_pb2_grpc.add_TransferServiceServicer_to_server(TransferService(), server)
    # Bind para toda a rede (necessário para acesso a partir de outra máquina)
    server.add_insecure_port(f"0.0.0.0:{TRANSFERS_SERVICE_PORT}")
    server.start()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} TransferService gRPC running on port {TRANSFERS_SERVICE_PORT} (Accounts at {ACCOUNTS_ADDR})")

    import signal
    def handle_signal(*_):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} Stopping transfers server...")
        server.stop(grace=5)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
