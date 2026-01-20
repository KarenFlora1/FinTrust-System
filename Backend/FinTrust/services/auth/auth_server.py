# FinTrust/services/auth/auth_server.py
import os
import grpc
from concurrent import futures
from datetime import datetime
import signal
import traceback

import auth_pb2
import auth_pb2_grpc
import auth_db

def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Login(self, request: auth_pb2.LoginRequest, context) -> auth_pb2.LoginResponse:
        try:
            username = (getattr(request, "username", "") or "").strip()
            password = (getattr(request, "password", "") or "").strip()
            resp = auth_pb2.LoginResponse()

            if not username or not password:
                resp.success = False; resp.token = ""; resp.message = "Missing credentials"; return resp

            dbuser = auth_db.get_user(username, password)
            if not dbuser:
                resp.success = False; resp.token = ""; resp.message = "invalid credentials"; return resp

            if isinstance(dbuser, dict):
                user_id = str(dbuser.get("user_id"))
            elif hasattr(dbuser, "user_id"):
                user_id = str(getattr(dbuser, "user_id"))
            else:
                try: user_id = str(dbuser[0])
                except Exception: user_id = None

            if not user_id:
                resp.success = False; resp.token = ""; resp.message = "invalid user record"; return resp

            token = f"token-{username}"
            try: auth_db.add_active_user(user_id, token)
            except Exception: traceback.print_exc()

            print(f"[Auth.Login] user_id={user_id} token={token}")
            resp.success = True; resp.token = token; resp.message = "logged successfully"
            return resp

        except Exception as e:
            traceback.print_exc()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            resp = auth_pb2.LoginResponse()
            resp.success = False; resp.token = ""; resp.message = "internal error"
            return resp

    def ValidateToken(self, request: auth_pb2.TokenRequest, context) -> auth_pb2.ValidateResponse:
        try:
            token = (getattr(request, "token", "") or "").strip()
            print(f"[Auth.ValidateToken] token={token!r}")
            resp = auth_pb2.ValidateResponse()

            if not token:
                resp.valid = False; resp.user_id = "0"; resp.message = "invalid token or expired"; return resp

            rec = auth_db.get_active_user(token)
            if not rec:
                resp.valid = False; resp.user_id = "0"; resp.message = "invalid token or expired"; return resp

            uid = str(rec.get("user_id", "0"))
            resp.valid = True; resp.user_id = uid; resp.message = "valid token"
            print(f"[Auth.ValidateToken] token={token!r} -> user_id={uid!r}")
            return resp

        except Exception as e:
            traceback.print_exc()
            resp = auth_pb2.ValidateResponse()
            resp.valid = False; resp.user_id = "0"; resp.message = f"internal error: {e}"
            return resp

def serve(port: int | None = None):
    AUTH_PORT = int(os.getenv("AUTH_PORT", port or 50051))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port(f"0.0.0.0:{AUTH_PORT}")
    server.start()
    print(f"{now_ts()} Running auth server on port {AUTH_PORT}")

    def handle_signal(*_):
        print(f"{now_ts()} Stopping auth server...")
        try: auth_db.clear_active_users()
        except Exception: traceback.print_exc()
        server.stop(grace=5)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
