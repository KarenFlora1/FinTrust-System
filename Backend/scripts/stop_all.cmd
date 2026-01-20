@echo off
taskkill /IM python.exe /F >nul 2>&1
taskkill /IM uvicorn.exe /F >nul 2>&1
echo [STOP] serviços terminados.
