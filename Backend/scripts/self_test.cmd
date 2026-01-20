@echo off
setlocal
echo ===== SELF TEST =====
where python
where pip
python --version
pip --version
echo venv activate...
call venv\Scripts\activate.bat || echo [WARN] venv ainda nao existe (ok apos setup_venv)
echo OK.
