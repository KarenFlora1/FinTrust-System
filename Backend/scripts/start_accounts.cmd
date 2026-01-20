@echo off
setlocal
cd /d "%~dp0..\FinTrust\services\accounts"
call ..\..\venv\Scripts\activate.bat || goto :error
if "%ACCOUNTS_PORT%"=="" set ACCOUNTS_PORT=50052
echo [ACCOUNTS] starting on 0.0.0.0:%ACCOUNTS_PORT%
set ACCOUNTS_PORT=%ACCOUNTS_PORT%
python accounts_server.py || goto :error
goto :eof
:error
echo [ACCOUNTS] ERRO
exit /b 1
