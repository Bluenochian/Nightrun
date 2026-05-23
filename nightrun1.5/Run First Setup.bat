@echo off
setlocal EnableExtensions
chcp 65001 >nul
color 0B
title Nightrun Setup

set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"
set "WORKFLOW=%~dp0"
set "REPO=%~dp0..\.."
set "PYTHON=%REPO%\venv\Scripts\python.exe"

echo.
echo ============================================================
echo   Nightrun Setup
echo ============================================================
echo   Creates config.local.json for this machine
echo   Detects GPU/VRAM, folders, models, and extensions
echo   Creates Desktop shortcuts for base run and upscaler
echo ============================================================
echo.

if not exist "%PYTHON%" (
  color 0E
  echo Forge venv Python was not found:
  echo "%PYTHON%"
  echo.
  echo Falling back to system python.
  set "PYTHON=python"
)

cd /d "%WORKFLOW%"
"%PYTHON%" "%WORKFLOW%setup_pipeline.py"
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
  color 0A
  echo Setup finished. Use Run Validation Stress Test.bat or Run One DRY TEST.bat next.
) else (
  color 0C
  echo Setup failed with exit code %RESULT%.
)

echo.
pause
