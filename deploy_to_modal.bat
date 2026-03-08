@echo off
echo ========================================
echo AI News Scraper - Modal Deployment
echo ========================================
echo.

cd /d "%~dp0"

echo Installing Modal CLI...
pip install modal

echo.
echo Logging into Modal...
modal token new

echo.
echo Deploying scraper...
modal deploy modal_scraper.py

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Your scraper is now scheduled to run every 3 hours.
echo Check: https://modal.com/dashboard
echo.
echo Dashboard: https://ai-news-scraper-3.vercel.app
echo.
pause
