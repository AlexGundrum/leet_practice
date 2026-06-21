@echo off
echo Starting AlgoRep...
echo.

:: Launch the Python HTTP server in a new window so you can easily close it later
start "AlgoRep Server" cmd /k "title AlgoRep Server && echo AlgoRep Local Server is running! && echo Close this window to stop the server. && echo. && python -m http.server 8000"

:: Wait for 1 second to give the server time to start up
timeout /t 1 /nobreak > NUL

:: Open the default web browser to the AlgoRep page
start http://localhost:8000/index.html
