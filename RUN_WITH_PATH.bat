@echo off
cd /d "%~dp0"
set "PYTHON_EXE=C:\Users\siddh\AppData\Local\Programs\Python\Python311\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python not found at: %PYTHON_EXE%
    echo Edit this file and set PYTHON_EXE to your python.exe path.
    pause
    exit /b 1
)

echo Using: %PYTHON_EXE%
"%PYTHON_EXE%" -m pip install -r requirements.txt -q
echo Starting API at http://127.0.0.1:8000
"%PYTHON_EXE%" run_api.py
pause
