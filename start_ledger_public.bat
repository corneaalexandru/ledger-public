@echo off
cd /d "%~dp0"
if "%LEDGER_HOST%"=="" set "LEDGER_HOST=127.0.0.1"
if "%LEDGER_PORT%"=="" set "LEDGER_PORT=8765"
py -m pip install -r requirements-google.txt
set "REQUESTED_PORT=%LEDGER_PORT%"
for /f %%P in ('py scripts\free_port.py "%LEDGER_HOST%" "%REQUESTED_PORT%" 2^>nul') do set "LEDGER_PORT=%%P"
if "%LEDGER_PORT%"=="" (
  echo No free port found from %REQUESTED_PORT% to %REQUESTED_PORT%+99.
  exit /b 1
)
if not "%LEDGER_PORT%"=="%REQUESTED_PORT%" echo Port %REQUESTED_PORT% is already in use. Using %LEDGER_PORT% instead.
py server.py --setup --store google --host "%LEDGER_HOST%" --port "%LEDGER_PORT%" --open
