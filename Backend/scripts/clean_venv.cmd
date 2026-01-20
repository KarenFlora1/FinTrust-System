@echo off
setlocal
echo [clean] removendo venv antiga...
rmdir /s /q venv >nul 2>&1
if exist venv echo [clean] ERRO ao apagar pasta && exit /b 1
echo [clean] OK
goto :eof
