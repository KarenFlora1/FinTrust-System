@echo off
setlocal
cd /d "%~dp0.."

echo Criando venv...
python -m venv venv

echo Activando venv...
call venv\Scripts\activate.bat

echo Instalando requirements...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Build local (se existir build.py)...
python build.py || echo [Aviso] Build.py falhou, verifique manualmente.

echo [OK] Setup completo.
endlocal
exit /b 0
