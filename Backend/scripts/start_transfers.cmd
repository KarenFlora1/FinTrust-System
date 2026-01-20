@echo off
setlocal
cd /d "%~dp0..\FinTrust\services\transfers"
call ..\..\venv\Scripts\activate.bat || goto :error

if "%TRANSFERS_PORT%"=="" set TRANSFERS_PORT=50053

REM Se SRV_IP estiver definido, usa-o como host do Accounts; caso contrario, localhost
if not "%SRV_IP%"=="" (
  set ACCOUNTS_ADDR=%SRV_IP%:50052
) else (
  if "%ACCOUNTS_ADDR%"=="" set ACCOUNTS_ADDR=127.0.0.1:50052
)

echo [TRANSFERS] starting on 0.0.0.0:%TRANSFERS_PORT% (Accounts=%ACCOUNTS_ADDR%)
set TRANSFERS_PORT=%TRANSFERS_PORT%
set ACCOUNTS_ADDR=%ACCOUNTS_ADDR%
python transfers_server.py || goto :error
goto :eof
:error
echo [TRANSFERS] ERRO
exit /b 1
