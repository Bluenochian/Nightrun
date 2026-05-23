@echo off
setlocal
title Nightrun - Prompt Variety Analyzer
color 0B
cls
set PYTHONUNBUFFERED=1
set PYTHONIOENCODING=utf-8
set "ROOT=%~dp0..\..\test-renders"
if not "%~1"=="" set "ROOT=%~1"
echo.
echo  Nightrun Prompt Variety Analyzer
echo  --------------------------------
echo  Scanning:
echo  %ROOT%
echo.
cd /d "%~dp0..\.."
"venv\Scripts\python.exe" "%~dp0tools\analyze_prompt_history.py" "%ROOT%" --report "%~dp0prompt_variety_report.json"
echo.
pause
