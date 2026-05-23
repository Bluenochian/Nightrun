@echo off
setlocal EnableExtensions
chcp 65001 >nul
color 0B
title Nightrun Upscaler

set "PYTHONUNBUFFERED=1"
set "PYTHONIOENCODING=utf-8"
set "WORKFLOW=%~dp0"
set "REPO=%~dp0..\.."
set "PYTHON=%REPO%\venv\Scripts\python.exe"
set "SCRIPT=%WORKFLOW%upscale_from_metadata.py"
set "CONFIG=config.json"
if exist "%WORKFLOW%config.local.json" set "CONFIG=config.local.json"

echo.
echo ============================================================
echo   Metadata Upscaler
echo ============================================================
echo   Existing image: used directly
echo   Missing image : recreated from metadata first
echo   Default scale : 2x from the selected source image
echo ============================================================
echo.

if not exist "%PYTHON%" (
  color 0E
  echo [warn] Forge venv Python was not found:
  echo        "%PYTHON%"
  echo        Trying system python instead.
  set "PYTHON=python"
  echo.
)

if not exist "%SCRIPT%" (
  color 0C
  echo [error] Script was not found:
  echo         "%SCRIPT%"
  goto done
)

if "%~1"=="" goto ask_path
goto run_dragged

:ask_path
echo Paste a *_metadata.json path below.
echo Tip: paths with non-English characters are supported.
echo.
set "META="
set /p "META=Metadata JSON path: "
if not defined META (
  color 0C
  echo [error] No path was entered.
  goto done
)
set "META=%META:"=%"
if not exist "%META%" (
  color 0C
  echo [error] Metadata file was not found:
  echo         "%META%"
  goto done
)

set "SCALE=2"
set /p "SCALE=Scale factor [2, 3, 4...]: "
if not defined SCALE set "SCALE=2"

cd /d "%REPO%"
echo.
echo [run] "%PYTHON%" "%SCRIPT%" "%META%" --config "%CONFIG%" --scale %SCALE%
echo.
"%PYTHON%" "%SCRIPT%" "%META%" --config "%CONFIG%" --scale %SCALE%
set "RESULT=%ERRORLEVEL%"
goto result

:run_dragged
cd /d "%REPO%"
echo [run] "%PYTHON%" "%SCRIPT%" %* --config "%CONFIG%" --scale 2
echo.
"%PYTHON%" "%SCRIPT%" %* --config "%CONFIG%" --scale 2
set "RESULT=%ERRORLEVEL%"
goto result

:result
echo.
if "%RESULT%"=="0" (
  color 0A
  echo [done] Finished successfully.
) else (
  color 0C
  echo [error] Upscale command failed with exit code %RESULT%.
)

:done
echo.
pause
