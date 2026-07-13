@echo off
echo Starting AlgoRep...
echo.

:: Run from the script's own directory so uvicorn can import server.py
cd /d "%~dp0"

:: Launch the FastAPI/uvicorn backend in a new window so you can easily close it later
start "AlgoRep Server" cmd /k "title AlgoRep Server && echo AlgoRep Local Server is running! && echo Close this window to stop the server. && echo. && python -m uvicorn server:app --host 127.0.0.1 --port 8000"

:: Wait for 1 second to give the server time to start up
timeout /t 1 /nobreak > NUL

:: Open the default web browser to the AlgoRep page
start http://localhost:8000/
