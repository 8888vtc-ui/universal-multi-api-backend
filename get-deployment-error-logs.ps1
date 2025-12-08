# get-deployment-error-logs.ps1
# Récupérer les logs d'erreur des déploiements Netlify

param(
    [string]$NetlifyToken = (Get-Content ".netlify-token" -ErrorAction SilentlyContinue),
    [int]$DeployId = 0
)

$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$API_BASE = "https://api.netlify.com/api/v1"

if (-not $NetlifyToken) {
    Write-Host "Erreur: Token Netlify non trouvé" -ForegroundColor Red
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $NetlifyToken"
    "Content-Type" = "application/json"
}

Write-Host "`n=== Logs d'Erreur des Déploiements ===`n" -ForegroundColor Cyan

try {
    # Récupérer les déploiements en erreur
    $deploys = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/deploys?per_page=10" -Method Get -Headers $headers
    
    $errorDeploys = $deploys | Where-Object { $_.state -eq "error" }
    
    if ($errorDeploys.Count -eq 0) {
        Write-Host "Aucun déploiement en erreur trouvé" -ForegroundColor Green
        exit 0
    }
    
    Write-Host "Déploiements en erreur trouvés: $($errorDeploys.Count)`n" -ForegroundColor Yellow
    
    foreach ($deploy in $errorDeploys) {
        Write-Host "=== Déploiement #$($deploy.id) ===" -ForegroundColor Red
        Write-Host "Date: $($deploy.created_at)" -ForegroundColor Gray
        Write-Host "Branch: $($deploy.branch)" -ForegroundColor Gray
        Write-Host "Commit: $($deploy.commit_ref)" -ForegroundColor Gray
        Write-Host ""
        
        # Récupérer les logs
        try {
            $logs = Invoke-RestMethod -Uri "$API_BASE/deploys/$($deploy.deploy_id)/log" -Method Get -Headers $headers
            if ($logs) {
                Write-Host "Logs d'erreur:" -ForegroundColor Yellow
                # Filtrer les lignes d'erreur
                $errorLines = $logs | Select-String -Pattern "error|Error|ERROR|failed|Failed|FAILED|warning|Warning|WARNING" -CaseSensitive:$false
                if ($errorLines) {
                    $errorLines | ForEach-Object {
                        Write-Host "  $_" -ForegroundColor Red
                    }
                } else {
                    Write-Host "  (Aucune ligne d'erreur spécifique trouvée)" -ForegroundColor Gray
                    # Afficher les dernières lignes
                    $logs | Select-Object -Last 20 | ForEach-Object {
                        Write-Host "  $_" -ForegroundColor Gray
                    }
                }
            } else {
                Write-Host "Logs non disponibles" -ForegroundColor Gray
            }
        } catch {
            Write-Host "Erreur lors de la récupération des logs: $_" -ForegroundColor Red
        }
        Write-Host ""
    }
    
} catch {
    Write-Host "Erreur: $_" -ForegroundColor Red
}


# Récupérer les logs d'erreur des déploiements Netlify

param(
    [string]$NetlifyToken = (Get-Content ".netlify-token" -ErrorAction SilentlyContinue),
    [int]$DeployId = 0
)

$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$API_BASE = "https://api.netlify.com/api/v1"

if (-not $NetlifyToken) {
    Write-Host "Erreur: Token Netlify non trouvé" -ForegroundColor Red
    exit 1
}

$headers = @{
    "Authorization" = "Bearer $NetlifyToken"
    "Content-Type" = "application/json"
}

Write-Host "`n=== Logs d'Erreur des Déploiements ===`n" -ForegroundColor Cyan

try {
    # Récupérer les déploiements en erreur
    $deploys = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/deploys?per_page=10" -Method Get -Headers $headers
    
    $errorDeploys = $deploys | Where-Object { $_.state -eq "error" }
    
    if ($errorDeploys.Count -eq 0) {
        Write-Host "Aucun déploiement en erreur trouvé" -ForegroundColor Green
        exit 0
    }
    
    Write-Host "Déploiements en erreur trouvés: $($errorDeploys.Count)`n" -ForegroundColor Yellow
    
    foreach ($deploy in $errorDeploys) {
        Write-Host "=== Déploiement #$($deploy.id) ===" -ForegroundColor Red
        Write-Host "Date: $($deploy.created_at)" -ForegroundColor Gray
        Write-Host "Branch: $($deploy.branch)" -ForegroundColor Gray
        Write-Host "Commit: $($deploy.commit_ref)" -ForegroundColor Gray
        Write-Host ""
        
        # Récupérer les logs
        try {
            $logs = Invoke-RestMethod -Uri "$API_BASE/deploys/$($deploy.deploy_id)/log" -Method Get -Headers $headers
            if ($logs) {
                Write-Host "Logs d'erreur:" -ForegroundColor Yellow
                # Filtrer les lignes d'erreur
                $errorLines = $logs | Select-String -Pattern "error|Error|ERROR|failed|Failed|FAILED|warning|Warning|WARNING" -CaseSensitive:$false
                if ($errorLines) {
                    $errorLines | ForEach-Object {
                        Write-Host "  $_" -ForegroundColor Red
                    }
                } else {
                    Write-Host "  (Aucune ligne d'erreur spécifique trouvée)" -ForegroundColor Gray
                    # Afficher les dernières lignes
                    $logs | Select-Object -Last 20 | ForEach-Object {
                        Write-Host "  $_" -ForegroundColor Gray
                    }
                }
            } else {
                Write-Host "Logs non disponibles" -ForegroundColor Gray
            }
        } catch {
            Write-Host "Erreur lors de la récupération des logs: $_" -ForegroundColor Red
        }
        Write-Host ""
    }
    
} catch {
    Write-Host "Erreur: $_" -ForegroundColor Red
}



