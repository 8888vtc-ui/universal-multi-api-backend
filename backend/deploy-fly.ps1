# Script de déploiement Fly.io avec timeout
Write-Host "=== Deploiement Fly.io ===" -ForegroundColor Green

# Vérifier que nous sommes dans le bon répertoire
if (-not (Test-Path "fly.toml")) {
    Write-Host "Erreur: fly.toml introuvable" -ForegroundColor Red
    Write-Host "Repertoire actuel: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n1. Verification de l'application..." -ForegroundColor Cyan
$appName = (Get-Content "fly.toml" | Select-String "app\s*=").ToString() -replace ".*app\s*=\s*['`"]?([^'`"]+)['`"]?.*", '$1'
Write-Host "   Application: $appName" -ForegroundColor White

Write-Host "`n2. Deploiement en cours..." -ForegroundColor Cyan
Write-Host "   (Cela peut prendre plusieurs minutes)" -ForegroundColor Yellow

# Déploiement avec timeout de 10 minutes
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD
    flyctl deploy --remote-only 2>&1
}

# Attendre avec timeout
$timeout = 600 # 10 minutes
$startTime = Get-Date
$completed = $false

while (-not $completed) {
    if ($job.State -eq "Completed" -or $job.State -eq "Failed") {
        $completed = $true
        $output = Receive-Job $job
        Write-Host $output
        Remove-Job $job
        break
    }
    
    $elapsed = (Get-Date) - $startTime
    if ($elapsed.TotalSeconds -gt $timeout) {
        Write-Host "`nTimeout atteint (10 minutes)" -ForegroundColor Red
        Stop-Job $job
        Remove-Job $job
        Write-Host "Le deploiement prend trop de temps." -ForegroundColor Yellow
        Write-Host "Essayez de deploiement manuel: flyctl deploy --remote-only" -ForegroundColor Yellow
        exit 1
    }
    
    Start-Sleep -Seconds 5
    Write-Host "." -NoNewline -ForegroundColor Gray
}

Write-Host "`n`n=== Deploiement termine ===" -ForegroundColor Green






