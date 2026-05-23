@echo off
setlocal
title Nightrun - Dry Test
color 0E
cls
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set "CONFIG=config.json"
if exist "%~dp0config.local.json" set "CONFIG=config.local.json"
if exist "%~dp0STOP_AFTER_CURRENT_IMAGE.txt" del /f /q "%~dp0STOP_AFTER_CURRENT_IMAGE.txt"
echo.
echo  Nightrun Dry Test
echo  -----------------
echo  Builds prompt metadata without sending images to Forge.
echo  Empty dry-run folders can be cleaned after the test.
echo.
cd /d "%~dp0..\.."
"venv\Scripts\python.exe" "%~dp0nightrun.py" --mode dry-run --count 5 --config "%CONFIG%"
pause
