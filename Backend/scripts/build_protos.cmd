@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."

echo === BUILDING PROTOS ===

REM Caminho base das pastas de serviços
set "BASE_DIR=%cd%\FinTrust\services"

for /d %%D in ("%BASE_DIR%\*") do (
    if exist "%%D\*.proto" (
        pushd "%%D"
        for %%f in (*.proto) do (
            echo Gerando para %%~nxf em %%D
            python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. "%%f"
        )
        popd
    )
)

echo [OK] Protos compilados.
endlocal
exit /b 0
