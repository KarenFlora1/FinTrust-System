@echo off
setlocal
cd /d "%~dp0..\FinTrust\services\auth"
call ..\..\venv\Scripts\activate.bat || goto :error
if "%AUTH_PORT%"=="" set AUTH_PORT=50051
echo [AUTH] starting on 0.0.0.0:%AUTH_PORT%
set AUTH_PORT=%AUTH_PORT%
python auth_server.py || goto :error
goto :eof
:error
echo [AUTH] ERRO
exit /b 1
