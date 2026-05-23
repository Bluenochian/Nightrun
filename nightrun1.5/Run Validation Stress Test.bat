@echo off
setlocal
title Nightrun - Validation
color 0A
cls
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set "CONFIG=config.json"
if exist "%~dp0config.local.json" set "CONFIG=config.local.json"
echo.
echo  Nightrun Validation
echo  -------------------
echo  Checks pools, LoRAs, and prompt formatting without generating images.
echo.
cd /d "%~dp0..\.."
"venv\Scripts\python.exe" "%~dp0nightrun.py" --mode validate --count 100 --config "%CONFIG%"
pause
