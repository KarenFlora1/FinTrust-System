@echo off
setlocal
cd /d "%~dp0..\FinTrust\gateway"
call ..\..\venv\Scripts\activate.bat || goto :error

REM ======= CONFIG DE REDE =======
if "%API_GATEWAY_HOST%"=="" set API_GATEWAY_HOST=0.0.0.0
if "%API_GATEWAY_PORT%"=="" set API_GATEWAY_PORT=8080

REM Se serviços estiverem noutra máquina, define SRV_IP (ex: 192.168.1.50).
if not "%SRV_IP%"=="" (
  set AUTH_ADDR=%SRV_IP%:50051
  set ACCOUNTS_ADDR=%SRV_IP%:50052
  set TRANSFERS_ADDR=%SRV_IP%:50053
) else (
  if "%AUTH_ADDR%"=="" set AUTH_ADDR=127.0.0.1:50051
  if "%ACCOUNTS_ADDR%"=="" set ACCOUNTS_ADDR=127.0.0.1:50052
  if "%TRANSFERS_ADDR%"=="" set TRANSFERS_ADDR=127.0.0.1:50053
)

if "%ALLOWED_ORIGINS%"=="" set ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

echo [GATEWAY] %API_GATEWAY_HOST%:%API_GATEWAY_PORT% (AUTH=%AUTH_ADDR% ACC=%ACCOUNTS_ADDR% TRF=%TRANSFERS_ADDR%)
set API_GATEWAY_HOST=%API_GATEWAY_HOST%
set API_GATEWAY_PORT=%API_GATEWAY_PORT%
set AUTH_ADDR=%AUTH_ADDR%
set ACCOUNTS_ADDR=%ACCOUNTS_ADDR%
set TRANSFERS_ADDR=%TRANSFERS_ADDR%
set ALLOWED_ORIGINS=%ALLOWED_ORIGINS%

python gateway.py || goto :error
goto :eof
:error
echo [GATEWAY] ERRO
exit /b 1
