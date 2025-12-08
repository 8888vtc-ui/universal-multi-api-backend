# check-deployment-logs.ps1
# Vérifier les logs de déploiement Netlify

param(
    [string]$NetlifyToken = (Get-Content ".netlify-token" -ErrorAction SilentlyContinue)
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

Write-Host "`n=== Logs de Déploiement Netlify ===`n" -ForegroundColor Cyan

try {
    # Récupérer les derniers déploiements
    $deploys = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/deploys?per_page=5" -Method Get -Headers $headers
    
    foreach ($deploy in $deploys) {
        Write-Host "Déploiement #$($deploy.id) - $($deploy.state)" -ForegroundColor Yellow
        Write-Host "  Date: $($deploy.created_at)" -ForegroundColor Gray
        Write-Host "  Branch: $($deploy.branch)" -ForegroundColor Gray
        Write-Host "  Commit: $($deploy.commit_ref)" -ForegroundColor Gray
        
        if ($deploy.state -eq "error") {
            Write-Host "  [ERREUR] Déploiement échoué!" -ForegroundColor Red
        } elseif ($deploy.state -eq "building") {
            Write-Host "  [EN COURS] Déploiement en cours..." -ForegroundColor Yellow
        } elseif ($deploy.state -eq "ready") {
            Write-Host "  [OK] Déploiement réussi" -ForegroundColor Green
        }
        
        # Récupérer les logs si disponibles
        if ($deploy.deploy_id) {
            try {
                $logs = Invoke-RestMethod -Uri "$API_BASE/deploys/$($deploy.deploy_id)/log" -Method Get -Headers $headers
                if ($logs) {
                    Write-Host "`n  Logs:" -ForegroundColor Cyan
                    $errorLines = $logs | Select-String -Pattern "error|Error|ERROR|failed|Failed|FAILED|warning|Warning" -CaseSensitive:$false
                    if ($errorLines) {
                        Write-Host "  Erreurs/Avertissements trouvés:" -ForegroundColor Red
                        $errorLines | Select-Object -First 10 | ForEach-Object {
                            Write-Host "    $_" -ForegroundColor Red
                        }
                    } else {
                        Write-Host "  Aucune erreur détectée dans les logs" -ForegroundColor Green
                    }
                }
            } catch {
                Write-Host "  Logs non disponibles" -ForegroundColor Gray
            }
        }
        Write-Host ""
    }
    
    # Vérifier le dernier déploiement en détail
    if ($deploys.Count -gt 0) {
        $latest = $deploys[0]
        Write-Host "=== Dernier Déploiement ===" -ForegroundColor Cyan
        Write-Host "State: $($latest.state)" -ForegroundColor $(if ($latest.state -eq "ready") { "Green" } elseif ($latest.state -eq "error") { "Red" } else { "Yellow" })
        Write-Host "URL: $($latest.deploy_ssl_url)" -ForegroundColor Cyan
        Write-Host "Build time: $($latest.deploy_time)s" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "Erreur lors de la récupération des logs: $_" -ForegroundColor Red
}


# Vérifier les logs de déploiement Netlify

param(
    [string]$NetlifyToken = (Get-Content ".netlify-token" -ErrorAction SilentlyContinue)
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

Write-Host "`n=== Logs de Déploiement Netlify ===`n" -ForegroundColor Cyan

try {
    # Récupérer les derniers déploiements
    $deploys = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/deploys?per_page=5" -Method Get -Headers $headers
    
    foreach ($deploy in $deploys) {
        Write-Host "Déploiement #$($deploy.id) - $($deploy.state)" -ForegroundColor Yellow
        Write-Host "  Date: $($deploy.created_at)" -ForegroundColor Gray
        Write-Host "  Branch: $($deploy.branch)" -ForegroundColor Gray
        Write-Host "  Commit: $($deploy.commit_ref)" -ForegroundColor Gray
        
        if ($deploy.state -eq "error") {
            Write-Host "  [ERREUR] Déploiement échoué!" -ForegroundColor Red
        } elseif ($deploy.state -eq "building") {
            Write-Host "  [EN COURS] Déploiement en cours..." -ForegroundColor Yellow
        } elseif ($deploy.state -eq "ready") {
            Write-Host "  [OK] Déploiement réussi" -ForegroundColor Green
        }
        
        # Récupérer les logs si disponibles
        if ($deploy.deploy_id) {
            try {
                $logs = Invoke-RestMethod -Uri "$API_BASE/deploys/$($deploy.deploy_id)/log" -Method Get -Headers $headers
                if ($logs) {
                    Write-Host "`n  Logs:" -ForegroundColor Cyan
                    $errorLines = $logs | Select-String -Pattern "error|Error|ERROR|failed|Failed|FAILED|warning|Warning" -CaseSensitive:$false
                    if ($errorLines) {
                        Write-Host "  Erreurs/Avertissements trouvés:" -ForegroundColor Red
                        $errorLines | Select-Object -First 10 | ForEach-Object {
                            Write-Host "    $_" -ForegroundColor Red
                        }
                    } else {
                        Write-Host "  Aucune erreur détectée dans les logs" -ForegroundColor Green
                    }
                }
            } catch {
                Write-Host "  Logs non disponibles" -ForegroundColor Gray
            }
        }
        Write-Host ""
    }
    
    # Vérifier le dernier déploiement en détail
    if ($deploys.Count -gt 0) {
        $latest = $deploys[0]
        Write-Host "=== Dernier Déploiement ===" -ForegroundColor Cyan
        Write-Host "State: $($latest.state)" -ForegroundColor $(if ($latest.state -eq "ready") { "Green" } elseif ($latest.state -eq "error") { "Red" } else { "Yellow" })
        Write-Host "URL: $($latest.deploy_ssl_url)" -ForegroundColor Cyan
        Write-Host "Build time: $($latest.deploy_time)s" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "Erreur lors de la récupération des logs: $_" -ForegroundColor Red
}



