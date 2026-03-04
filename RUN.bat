@echo off
cd /d "%~dp0"

set "PY=C:\Users\siddh\AppData\Local\Programs\Python\Python311\python.exe"
set "PYDIR=C:\Users\siddh\AppData\Local\Programs\Python\Python311"
set "PATH=%PYDIR%;%PYDIR%\Scripts;%PATH%"

if not exist "%PY%" (
    echo Python not found at %PY%
    echo Edit RUN.bat and set PY= to your python.exe path.
    pause
    exit /b 1
)

echo Using: %PY%
echo Installing deps...
"%PY%" -m pip install --user -r requirements.txt -q
if errorlevel 1 (echo Pip failed. & pause & exit /b 1)
echo Starting API at http://127.0.0.1:8000
"%PY%" run_api.py
pause
