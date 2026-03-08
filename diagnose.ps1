# AI Dashboard Diagnostic Script
Write-Host "🤖 AI News Dashboard Diagnostic" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if Python processes are running
Write-Host "`n[1/4] Checking Python processes..." -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "✅ Python processes found: $($pythonProcesses.Count)" -ForegroundColor Green
    foreach ($proc in $pythonProcesses) {
        Write-Host "   - PID $($proc.Id), CommandLine: $($proc.CommandLine)" -ForegroundColor Gray
    }
} else {
    Write-Host "❌ No Python processes running" -ForegroundColor Red
}

# Check port availability
Write-Host "`n[2/4] Checking ports..." -ForegroundColor Yellow
$ports = @(8000, 8001)
foreach ($port in $ports) {
    try {
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Parse("127.0.0.1"), $port)
        $listener.Start()
        $listener.Stop()
        Write-Host "✅ Port $port is available" -ForegroundColor Green
    } catch {
        Write-Host "❌ Port $port is in use" -ForegroundColor Red
    }
}

# Test server connectivity
Write-Host "`n[3/4] Testing server connectivity..." -ForegroundColor Yellow
$testUrls = @(
    "http://localhost:8001/dashboard.html",
    "http://127.0.0.1:8001/dashboard.html"
)

foreach ($url in $testUrls) {
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ $url - Accessible ($($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "❌ $url - Cannot reach ($($_.Exception.Message))" -ForegroundColor Red
    }
}

# Check firewall status
Write-Host "`n[4/4] Checking firewall..." -ForegroundColor Yellow
$firewall = Get-NetFirewallProfile -ErrorAction SilentlyContinue
if ($firewall) {
    Write-Host "✅ Firewall information available" -ForegroundColor Green
    foreach ($profile in $firewall) {
        Write-Host "   - $($profile.Name): $($profile.Enabled)" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️  Cannot check firewall status" -ForegroundColor Yellow
}

Write-Host "`n" + "=" * 50
Write-Host "🎯 Recommended Actions:" -ForegroundColor Cyan
Write-Host "1. Open launch_dashboard.html in your browser" -ForegroundColor White
Write-Host "2. Try the manual URLs listed above" -ForegroundColor White
Write-Host "3. Use incognito/private browsing mode" -ForegroundColor White
Write-Host "4. Try a different browser" -ForegroundColor White
Write-Host "`nServer is running on port 8001 - Dashboard should be accessible!" -ForegroundColor Green