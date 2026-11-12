@echo off
setlocal
cd /d "%~dp0"
type nul > "STOP_AFTER_CURRENT_IMAGE.txt"
echo Stop signal created.
echo Nightrun will finish the current image, then stop before starting the next one.
pause
