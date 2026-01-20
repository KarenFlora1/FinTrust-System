@echo off
setlocal
cd /d "%~dp0.."

echo === MIGRANDO BASE DE DADOS ===

if not exist "venv\Scripts\activate.bat" (
    echo [ERRO] venv nao existe. Corre setup_venv primeiro.
    exit /b 1
)
call venv\Scripts\activate.bat

if exist migrate.py (
    echo [info] Executando migrate.py...
    python migrate.py || goto :error
    goto :ok
)

echo [info] Nenhum migrate.py encontrado. Nada a migrar.
goto :ok

:error
echo [ERRO] Erro durante a migracao!
exit /b 1

:ok
echo [OK] Migracao concluida.
endlocal
exit /b 0
