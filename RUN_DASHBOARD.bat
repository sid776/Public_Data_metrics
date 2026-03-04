@echo off
cd /d "%~dp0"
set "PY=C:\Users\siddh\AppData\Local\Programs\Python\Python311\python.exe"
set "PATH=C:\Users\siddh\AppData\Local\Programs\Python\Python311;C:\Users\siddh\AppData\Local\Programs\Python\Python311\Scripts;%PATH%"

"%PY%" -m pip install plotly pandas -q 2>nul
echo Opening Dashboard at http://localhost:8502
"%PY%" -m streamlit run dashboard.py --server.port 8502
pause
