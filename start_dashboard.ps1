# AI News Dashboard Launcher
Write-Host "🤖 Starting AI News Dashboard..." -ForegroundColor Cyan

# Kill any existing Python processes
Write-Host "Stopping any existing servers..." -ForegroundColor Yellow
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

# Start HTTP server
Write-Host "Starting HTTP server on port 8000..." -ForegroundColor Yellow
$serverProcess = Start-Process python -ArgumentList "-m http.server 8000 --bind localhost --directory ." -WindowStyle Hidden -PassThru

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Open dashboard
Write-Host "Opening dashboard..." -ForegroundColor Green
Start-Process "http://localhost:8000/"

Write-Host "`n🎉 Dashboard should open automatically!" -ForegroundColor Green
Write-Host "If it doesn't open, manually go to: http://localhost:8000/" -ForegroundColor Yellow
Write-Host "`nPress Enter to stop the server..." -ForegroundColor White
$null = Read-Host

Write-Host "Stopping server..." -ForegroundColor Yellow
Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
Write-Host "Server stopped." -ForegroundColor Green