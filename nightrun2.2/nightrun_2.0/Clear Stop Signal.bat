@echo off
setlocal
cd /d "%~dp0"
if exist "STOP_AFTER_CURRENT_IMAGE.txt" (
  del "STOP_AFTER_CURRENT_IMAGE.txt"
  echo Stop signal cleared.
) else (
  echo No stop signal was present.
)
pause
