@echo off
setlocal
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONUTF8=1"
if not exist ".venv\Scripts\python.exe" (
    echo Python environment missing. See README.md for setup.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" "src\vision_lab\main.py" --threshold 0.4 --save-crops --save-preview --no-show %*
set "vision_exit_code=%errorlevel%"
echo.
if not "%vision_exit_code%"=="0" echo Execution failed. Exit code: %vision_exit_code%
pause
exit /b %vision_exit_code%
