@echo off
cd /d "%~dp0.."
setlocal

echo === INICIANDO SERVIÇOS FINTRUST ===

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat || (
    echo [ERRO] venv nao encontrado. Corre primeiro: scripts\setup_venv.cmd
    exit /b 1
)

start "AUTH" cmd /c "cd FinTrust\services\auth && python auth_server.py"
start "ACCOUNTS" cmd /c "cd FinTrust\services\accounts && python accounts_server.py"
start "TRANSFERS" cmd /c "cd FinTrust\services\transfers && python transfers_server.py"

timeout /t 5 >nul

echo Iniciando API Gateway...
start "GATEWAY" cmd /c "cd FinTrust\gateway && python gateway.py"

echo [OK] Todos os serviços foram iniciados!
echo ============================================
echo - Auth:       porta 50051
echo - Accounts:   porta 50052
echo - Transfers:  porta 50053
echo - Gateway:    porta 8080
echo ============================================

endlocal
exit /b 0
