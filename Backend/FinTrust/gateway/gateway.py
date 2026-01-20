# FinTrust/gateway/gateway.py
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import grpc
import os, sys
import sqlite3
from datetime import datetime

# ----- paths dos serviços (mantém) -----
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'auth'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'accounts'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'services', 'transfers'))

import auth_pb2, auth_pb2_grpc
import accounts_pb2, accounts_pb2_grpc
import transfers_pb2, transfers_pb2_grpc

# ======= CONFIG =======
API_GATEWAY_HOST = os.getenv("API_GATEWAY_HOST", "0.0.0.0")
API_GATEWAY_PORT = int(os.getenv("API_GATEWAY_PORT", "8080"))

# Endereços dos serviços (permite 2 máquinas)
AUTH_ADDR      = os.getenv("AUTH_ADDR",      "127.0.0.1:50051")
ACCOUNTS_ADDR  = os.getenv("ACCOUNTS_ADDR",  "127.0.0.1:50052")
TRANSFERS_ADDR = os.getenv("TRANSFERS_ADDR", "127.0.0.1:50053")

# CORS (origens permitidas)
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS",
                            "http://localhost:5173,http://127.0.0.1:5173").split(",")

# ======= gRPC Stubs =======
auth_channel     = grpc.insecure_channel(AUTH_ADDR)
auth_stub        = auth_pb2_grpc.AuthServiceStub(auth_channel)

accounts_channel = grpc.insecure_channel(ACCOUNTS_ADDR)
accounts_stub    = accounts_pb2_grpc.AccountsServiceStub(accounts_channel)

transfers_channel= grpc.insecure_channel(TRANSFERS_ADDR)
transfers_stub   = transfers_pb2_grpc.TransferServiceStub(transfers_channel)

# ======= FastAPI =======
app = FastAPI(title="FinTrust API Gateway")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in ALLOWED_ORIGINS if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- DB do histórico (local ao gateway) -----
HIST_DB = os.path.join(os.path.dirname(__file__), "history.db")

def _hist_conn():
    return sqlite3.connect(HIST_DB)

def _hist_init():
    con = _hist_conn(); cur = con.cursor()
    cur.execute("""
      CREATE TABLE IF NOT EXISTS transfers_history (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        ts           TEXT    NOT NULL,
        from_account INTEGER NOT NULL,
        to_account   INTEGER NOT NULL,
        amount       REAL    NOT NULL,
        token        TEXT,
        user_id      TEXT
      )
    """)
    con.commit(); con.close()

def _hist_add(ts: str, from_acc: int, to_acc: int, amount: float, token: str, user_id: str):
    con = _hist_conn(); cur = con.cursor()
    cur.execute(
        "INSERT INTO transfers_history(ts, from_account, to_account, amount, token, user_id) VALUES (?,?,?,?,?,?)",
        (ts, int(from_acc), int(to_acc), float(amount), token, str(user_id))
    )
    con.commit(); con.close()

_hist_init()

# ----- models -----
class LoginData(BaseModel):
    username: str
    password: str

class TransferData(BaseModel):
    from_account: int
    to_account: int
    amount: float

# ========== endpoints ==========
@app.post('/login')
def login(data: LoginData):
    try:
        req = auth_pb2.LoginRequest()
        req.username = data.username
        req.password = data.password
        response = auth_stub.Login(req)
    except grpc.RpcError as e:
        print("AUTH RPC ERROR (Login):", e.code(), e.details())
        raise HTTPException(status_code=502, detail="Auth service is unavailable")
    except Exception as e:
        print("AUTH ERROR (Login):", repr(e))
        raise HTTPException(status_code=502, detail="Auth service is unavailable")

    if not response.success:
        raise HTTPException(status_code=401, detail=response.message)

    return {"token": response.token}


@app.get('/accounts')
def list_accounts(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    token = authorization.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    # 1) validar token no Auth
    try:
        t = auth_pb2.TokenRequest(); t.token = token
        val_resp = auth_stub.ValidateToken(t)
        print("[GATEWAY] token=", token,
              "valid=", getattr(val_resp, "valid", None),
              "user_id=", repr(getattr(val_resp, "user_id", None)))
    except grpc.RpcError as e:
        print("AUTH RPC ERROR (ValidateToken):", e.code(), e.details())
        raise HTTPException(status_code=502, detail="Auth service unavailable")
    except Exception as e:
        print("AUTH ERROR (ValidateToken):", repr(e))
        raise HTTPException(status_code=502, detail="Auth service unavailable")

    if not getattr(val_resp, "valid", False):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id_str = str(getattr(val_resp, "user_id", "0") or "0")
    if user_id_str in ("", "0"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # 2) buscar contas
    try:
        req = accounts_pb2.UserRequest(); req.user_id = user_id_str
        acc_resp = accounts_stub.ListAccounts(req)
    except grpc.RpcError as e:
        print("ACCOUNTS RPC ERROR (ListAccounts):", e.code(), e.details())
        raise HTTPException(status_code=502, detail="Accounts service is unavailable")
    except Exception as e:
        print("ACCOUNTS ERROR (ListAccounts):", repr(e))
        raise HTTPException(status_code=502, detail="Accounts service is unavailable")

    accounts_list = [{"id": a.id, "balance": a.balance} for a in acc_resp.accounts]
    return {"accounts": accounts_list}


@app.post("/transfer")
def make_transfer(data: TransferData, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization token")

    token = authorization.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    # validar token
    try:
        t = auth_pb2.TokenRequest(); t.token = token
        val_resp = auth_stub.ValidateToken(t)
    except grpc.RpcError as e:
        print("AUTH RPC ERROR (ValidateToken):", e.code(), e.details())
        raise HTTPException(status_code=502, detail="Auth service unavailable")
    except Exception as e:
        print("AUTH ERROR (ValidateToken):", repr(e))
        raise HTTPException(status_code=502, detail="Auth service unavailable")

    if not getattr(val_resp, "valid", False):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id_str = str(getattr(val_resp, "user_id", "0") or "0")
    if user_id_str in ("", "0"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # obter contas do user para checar ownership
    try:
        req_user = accounts_pb2.UserRequest(); req_user.user_id = user_id_str
        user_accounts = accounts_stub.ListAccounts(req_user)
    except grpc.RpcError as e:
        print("ACCOUNTS RPC ERROR (ListAccounts for transfer):", e.code(), e.details())
        raise HTTPException(status_code=502, detail="Accounts service is unavailable")
    except Exception as e:
        print("ACCOUNTS ERROR (ListAccounts for transfer):", repr(e))
        raise HTTPException(status_code=502, detail="Accounts service is unavailable")

    owned_ids = [acc.id for acc in user_accounts.accounts]
    if data.from_account not in owned_ids:
        raise HTTPException(status_code=403, detail="Cannot transfer from an account you don't own")

    # efetuar transferência
    try:
        treq = transfers_pb2.TransferRequest()
        treq.from_account_id = data.from_account
        treq.to_account_id   = data.to_account
        treq.amount          = float(data.amount)
        trans_resp = transfers_stub.MakeTransfer(treq)
    except grpc.RpcError as e:
        print("TRANSFERS RPC ERROR (MakeTransfer):", e.code(), e.details())
        raise HTTPException(status_code=502, detail="Transfer service unavailable")
    except Exception as e:
        print("TRANSFERS ERROR (MakeTransfer):", repr(e))
        raise HTTPException(status_code=502, detail="Transfer service unavailable")

    if not getattr(trans_resp, "success", False):
        raise HTTPException(status_code=400, detail=getattr(trans_resp, "message", "transfer failed"))

    try:
        _hist_add(
            ts=datetime.utcnow().isoformat(timespec="seconds"),
            from_acc=data.from_account,
            to_acc=data.to_account,
            amount=float(data.amount),
            token=token,
            user_id=user_id_str
        )
    except Exception:
        pass

    return {"transaction_id": trans_resp.transaction_id, "message": trans_resp.message}


@app.get("/history")
def list_history(authorization: str = Header(None), limit: int = 50):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")

    token = authorization.strip()
    if token.lower().startswith("bearer "):
        token = token[7:].strip()

    try:
        t = auth_pb2.TokenRequest(); t.token = token
        val_resp = auth_stub.ValidateToken(t)
    except grpc.RpcError:
        raise HTTPException(status_code=502, detail="Auth service unavailable")
    if not getattr(val_resp, "valid", False):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id_str = str(getattr(val_resp, "user_id", "0") or "0")
    if user_id_str in ("", "0"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    req = accounts_pb2.UserRequest(); req.user_id = user_id_str
    try:
        acc_resp = accounts_stub.ListAccounts(req)
    except grpc.RpcError:
        raise HTTPException(status_code=502, detail="Accounts service is unavailable")

    owned_ids = [a.id for a in acc_resp.accounts]
    if not owned_ids:
        return {"items": []}

    placeholders = ",".join("?" for _ in owned_ids)
    sql = f"""
      SELECT ts, from_account, to_account, amount
      FROM transfers_history
      WHERE from_account IN ({placeholders})
         OR to_account   IN ({placeholders})
      ORDER BY id DESC
      LIMIT ?
    """
    con = _hist_conn(); cur = con.cursor()
    rows = cur.execute(sql, (*owned_ids, *owned_ids, int(limit))).fetchall()
    con.close()

    items = [{"ts": r[0], "from_account": r[1], "to_account": r[2], "amount": r[3]} for r in rows]
    return {"items": items}

# ----- execução direta -----
if __name__ == '__main__':
    import uvicorn, signal
    now = datetime.now()
    print(f'{now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]} Starting the api gateway on {API_GATEWAY_HOST}:{API_GATEWAY_PORT}')

    def handle_signal(*_):
        n = datetime.now()
        print(f'{n.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]} Stopping gateway server...')

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    uvicorn.run("gateway:app", host=API_GATEWAY_HOST, port=API_GATEWAY_PORT, reload=True)
