@echo off
echo Starting AI News Dashboard...

REM Kill any existing Python processes
taskkill /f /im python.exe >nul 2>&1

REM Start the HTTP server
python -m http.server 8000 --bind localhost --directory .