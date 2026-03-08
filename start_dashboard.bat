@echo off
echo Starting AI News Dashboard...
echo.

REM Kill any existing Python processes
echo Stopping any existing servers...
taskkill /f /im python.exe >nul 2>&1

REM Start the HTTP server on port 8000
echo Starting HTTP server on port 8000...
start /b python -m http.server 8000 --bind localhost --directory .

REM Wait for server to start
echo Waiting for server to start...
ping -n 3 127.0.0.1 >nul

REM Open the dashboard page
echo Opening dashboard...
start "" "http://localhost:8000/"

echo.
echo ========================================
echo Dashboard should open automatically!
echo ========================================
echo.
echo If it doesn't open automatically:
echo 1. Open your web browser
echo 2. Go to: http://localhost:8000/
echo 3. Or try: http://127.0.0.1:8000/
echo.
echo Press any key to stop the server...
pause >nul

echo.
echo Stopping server...
taskkill /f /im python.exe >nul 2>&1
echo Server stopped.
echo.