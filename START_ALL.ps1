# Universal API Hub - Script de démarrage PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Universal API Hub - Demarrage" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Démarrer le backend
Write-Host "[1/2] Demarrage du Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; python main.py"

# Attendre
Write-Host "Attente du demarrage du backend (10s)..." -ForegroundColor Gray
Start-Sleep -Seconds 10

# Vérifier si node_modules existe
if (-not (Test-Path "$PSScriptRoot\frontend\node_modules")) {
    Write-Host "[!] Installation des dependances npm..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm install; npm run dev" -Wait:$false
} else {
    Write-Host "[2/2] Demarrage du Frontend..." -ForegroundColor Yellow
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Tout est demarre!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Docs:     http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur une touche pour fermer..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")






