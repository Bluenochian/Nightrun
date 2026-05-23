@echo off
setlocal
title Nightrun - Base
color 0B
cls
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set "CONFIG=config.json"
if exist "%~dp0config.local.json" set "CONFIG=config.local.json"
if exist "%~dp0STOP_AFTER_CURRENT_IMAGE.txt" del /f /q "%~dp0STOP_AFTER_CURRENT_IMAGE.txt"
echo.
echo  Nightrun
echo  --------
echo  Mode   : base images, with low-step upscale if enabled
echo  Config : %CONFIG%
echo.
cd /d "%~dp0..\.."
"venv\Scripts\python.exe" "%~dp0nightrun.py" --mode base --config "%CONFIG%"
pause
