# check-netlify-vars.ps1
# Vérifier les valeurs des variables Netlify

param(
    [Parameter(Mandatory=$true)]
    [string]$NetlifyToken
)

$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$API_BASE = "https://api.netlify.com/api/v1"

$headers = @{
    "Authorization" = "Bearer $NetlifyToken"
    "Content-Type" = "application/json"
}

Write-Host "`n=== Variables Netlify ===`n" -ForegroundColor Cyan

try {
    $vars = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env" -Method Get -Headers $headers
    
    foreach ($var in $vars) {
        Write-Host "$($var.key):" -ForegroundColor Yellow
        foreach ($value in $var.values) {
            $context = $value.context
            $val = $value.value
            Write-Host "  [$context] = $val" -ForegroundColor White
        }
        Write-Host ""
    }
    
    # Vérifier les valeurs attendues
    Write-Host "=== Verification ===" -ForegroundColor Cyan
    
    $expected = @{
        "NEXT_PUBLIC_API_URL" = "https://universal-api-hub.fly.dev"
        "NEXT_PUBLIC_APP_NAME" = "WikiAsk"
        "NEXT_PUBLIC_APP_SLOGAN" = "Ask Everything. Know Everything."
    }
    
    $allOk = $true
    foreach ($key in $expected.Keys) {
        $var = $vars | Where-Object { $_.key -eq $key }
        if ($var) {
            # Chercher d'abord production, puis all, puis n'importe quelle valeur
            $prodValue = ($var.values | Where-Object { $_.context -eq "production" }).value
            if (-not $prodValue) {
                $prodValue = ($var.values | Where-Object { $_.context -eq "all" }).value
            }
            if (-not $prodValue -and $var.values.Count -gt 0) {
                $prodValue = $var.values[0].value
            }
            
            if ($prodValue -eq $expected[$key]) {
                Write-Host "[OK] $key = $prodValue" -ForegroundColor Green
            } else {
                Write-Host "[ERREUR] $key = '$prodValue' (attendu: '$($expected[$key])')" -ForegroundColor Red
                $allOk = $false
            }
        } else {
            Write-Host "[MANQUANT] $key" -ForegroundColor Red
            $allOk = $false
        }
    }
    
    if ($allOk) {
        Write-Host "`n[OK] Toutes les variables sont correctement configurees!" -ForegroundColor Green
    } else {
        Write-Host "`n[ATTENTION] Certaines variables doivent etre corrigees" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Erreur: $_" -ForegroundColor Red
}



param(
    [Parameter(Mandatory=$true)]
    [string]$NetlifyToken
)

$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$API_BASE = "https://api.netlify.com/api/v1"

$headers = @{
    "Authorization" = "Bearer $NetlifyToken"
    "Content-Type" = "application/json"
}

Write-Host "`n=== Variables Netlify ===`n" -ForegroundColor Cyan

try {
    $vars = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env" -Method Get -Headers $headers
    
    foreach ($var in $vars) {
        Write-Host "$($var.key):" -ForegroundColor Yellow
        foreach ($value in $var.values) {
            $context = $value.context
            $val = $value.value
            Write-Host "  [$context] = $val" -ForegroundColor White
        }
        Write-Host ""
    }
    
    # Vérifier les valeurs attendues
    Write-Host "=== Verification ===" -ForegroundColor Cyan
    
    $expected = @{
        "NEXT_PUBLIC_API_URL" = "https://universal-api-hub.fly.dev"
        "NEXT_PUBLIC_APP_NAME" = "WikiAsk"
        "NEXT_PUBLIC_APP_SLOGAN" = "Ask Everything. Know Everything."
    }
    
    $allOk = $true
    foreach ($key in $expected.Keys) {
        $var = $vars | Where-Object { $_.key -eq $key }
        if ($var) {
            # Chercher d'abord production, puis all, puis n'importe quelle valeur
            $prodValue = ($var.values | Where-Object { $_.context -eq "production" }).value
            if (-not $prodValue) {
                $prodValue = ($var.values | Where-Object { $_.context -eq "all" }).value
            }
            if (-not $prodValue -and $var.values.Count -gt 0) {
                $prodValue = $var.values[0].value
            }
            
            if ($prodValue -eq $expected[$key]) {
                Write-Host "[OK] $key = $prodValue" -ForegroundColor Green
            } else {
                Write-Host "[ERREUR] $key = '$prodValue' (attendu: '$($expected[$key])')" -ForegroundColor Red
                $allOk = $false
            }
        } else {
            Write-Host "[MANQUANT] $key" -ForegroundColor Red
            $allOk = $false
        }
    }
    
    if ($allOk) {
        Write-Host "`n[OK] Toutes les variables sont correctement configurees!" -ForegroundColor Green
    } else {
        Write-Host "`n[ATTENTION] Certaines variables doivent etre corrigees" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "Erreur: $_" -ForegroundColor Red
}

