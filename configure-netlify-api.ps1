# configure-netlify-api.ps1
# Configuration Netlify via API (plus fiable que CLI)

param(
    [Parameter(Mandatory=$true)]
    [string]$NetlifyToken,
    [switch]$Force = $false
)

$ErrorActionPreference = "Continue"

$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$API_BASE = "https://api.netlify.com/api/v1"

function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "Configuration Netlify via API"
Write-Info "============================"

# Headers pour l'API
$headers = @{
    "Authorization" = "Bearer $NetlifyToken"
    "Content-Type" = "application/json"
}

# Variables à configurer
$variables = @{
    "NEXT_PUBLIC_API_URL" = "https://universal-api-hub.fly.dev"
    "NEXT_PUBLIC_APP_NAME" = "WikiAsk"
    "NEXT_PUBLIC_APP_SLOGAN" = "Ask Everything. Know Everything."
}

# Contextes Netlify
$contexts = @("production", "deploy-preview", "branch-deploy")

# Fonction pour obtenir les variables existantes
function Get-ExistingVariables {
    try {
        $response = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env" -Method Get -Headers $headers
        return $response
    } catch {
        Write-Warning "Impossible de récupérer les variables existantes: $_"
        return @()
    }
}

# Fonction pour créer/mettre à jour une variable
function Set-NetlifyVariable {
    param(
        [string]$Key,
        [string]$Value,
        [string[]]$Contexts
    )
    
    Write-Info "`nConfiguration de $Key = $Value"
    
    # Créer les valeurs pour chaque contexte
    $values = @()
    foreach ($context in $Contexts) {
        $values += @{
            value = $Value
            context = $context
        }
        Write-Info "  → Contexte: $context"
    }
    
    $body = @{
        key = $Key
        values = $values
    } | ConvertTo-Json -Depth 10
    
    try {
        # Vérifier si la variable existe déjà
        $existing = Get-ExistingVariables | Where-Object { $_.key -eq $Key }
        
        if ($existing -and -not $Force) {
            Write-Warning "  Variable $Key existe déjà"
            Write-Info "  Utilisez -Force pour la mettre à jour"
            return $false
        }
        
        # Si existe et Force, supprimer d'abord
        if ($existing -and $Force) {
            Write-Info "  Suppression de l'ancienne variable..."
            try {
                Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env/$($existing.id)" -Method Delete -Headers $headers | Out-Null
                Write-Success "  ✅ Ancienne variable supprimée"
            } catch {
                Write-Warning "  Impossible de supprimer l'ancienne variable (peut-être déjà supprimée)"
            }
        }
        
        # Créer la nouvelle variable
        Write-Info "  Création de la variable..."
        $response = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env" -Method Post -Headers $headers -Body $body
        
        Write-Success "  ✅ Variable $Key configurée avec succès"
        return $true
        
    } catch {
        $errorDetails = $_.ErrorDetails.Message
        if ($errorDetails) {
            try {
                $errorJson = $errorDetails | ConvertFrom-Json
                if ($errorJson.message) {
                    Write-Error "  ❌ Erreur: $($errorJson.message)"
                } else {
                    Write-Error "  ❌ Erreur: $errorDetails"
                }
            } catch {
                Write-Error "  ❌ Erreur: $errorDetails"
            }
        } else {
            Write-Error "  ❌ Erreur: $_"
        }
        return $false
    }
}

# Vérifier le token
Write-Info "`nVérification du token..."
try {
    $user = Invoke-RestMethod -Uri "$API_BASE/user" -Method Get -Headers $headers
    Write-Success "✅ Token valide - Connecté en tant que: $($user.email)"
} catch {
    Write-Error "❌ Token invalide ou expiré"
    Write-Info "💡 Obtenez un nouveau token sur: https://app.netlify.com/user/applications"
    exit 1
}

# Vérifier l'accès au site
Write-Info "`nVérification de l'accès au site..."
try {
    $site = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID" -Method Get -Headers $headers
    Write-Success "✅ Accès au site confirmé: $($site.name)"
    Write-Info "   URL: $($site.url)"
} catch {
    Write-Error "❌ Impossible d'accéder au site. Vérifiez le SITE_ID et les permissions du token"
    exit 1
}

# Lister les variables existantes
Write-Info "`nVariables existantes:"
$existingVars = Get-ExistingVariables
if ($existingVars) {
    foreach ($var in $existingVars) {
        $contextsStr = ($var.values | ForEach-Object { $_.context }) -join ", "
        Write-Host "  - $($var.key) [$contextsStr]" -ForegroundColor Gray
    }
} else {
    Write-Info "  Aucune variable configurée"
}

# Configurer chaque variable
Write-Info "`nConfiguration des variables..."
$successCount = 0
$failCount = 0

foreach ($varName in $variables.Keys) {
    $varValue = $variables[$varName]
    $success = Set-NetlifyVariable -Key $varName -Value $varValue -Contexts $contexts
    if ($success) {
        $successCount++
    } else {
        $failCount++
    }
}

# Résumé
Write-Info "`n=== Résumé ==="
Write-Success "✅ Variables configurées avec succès: $successCount"
if ($failCount -gt 0) {
    Write-Warning "⚠️ Variables en échec: $failCount"
}

# Vérification finale
Write-Info "`nVérification finale:"
$finalVars = Get-ExistingVariables
$configuredVars = @()
foreach ($varName in $variables.Keys) {
    $found = $finalVars | Where-Object { $_.key -eq $varName }
    if ($found) {
        $configuredVars += $varName
        Write-Success "  ✅ $varName configurée"
    } else {
        Write-Warning "  ⚠️ $varName non trouvée"
    }
}

Write-Info "`n=== Configuration terminée ==="
Write-Info "💡 Redéployez le site dans Netlify Dashboard pour appliquer les changements"
Write-Info "   URL: https://app.netlify.com/projects/$SITE_ID/deploys"


# Configuration Netlify via API (plus fiable que CLI)

param(
    [Parameter(Mandatory=$true)]
    [string]$NetlifyToken,
    [switch]$Force = $false
)

$ErrorActionPreference = "Continue"

$SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$API_BASE = "https://api.netlify.com/api/v1"

function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "Configuration Netlify via API"
Write-Info "============================"

# Headers pour l'API
$headers = @{
    "Authorization" = "Bearer $NetlifyToken"
    "Content-Type" = "application/json"
}

# Variables à configurer
$variables = @{
    "NEXT_PUBLIC_API_URL" = "https://universal-api-hub.fly.dev"
    "NEXT_PUBLIC_APP_NAME" = "WikiAsk"
    "NEXT_PUBLIC_APP_SLOGAN" = "Ask Everything. Know Everything."
}

# Contextes Netlify
$contexts = @("production", "deploy-preview", "branch-deploy")

# Fonction pour obtenir les variables existantes
function Get-ExistingVariables {
    try {
        $response = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env" -Method Get -Headers $headers
        return $response
    } catch {
        Write-Warning "Impossible de récupérer les variables existantes: $_"
        return @()
    }
}

# Fonction pour créer/mettre à jour une variable
function Set-NetlifyVariable {
    param(
        [string]$Key,
        [string]$Value,
        [string[]]$Contexts
    )
    
    Write-Info "`nConfiguration de $Key = $Value"
    
    # Créer les valeurs pour chaque contexte
    $values = @()
    foreach ($context in $Contexts) {
        $values += @{
            value = $Value
            context = $context
        }
        Write-Info "  → Contexte: $context"
    }
    
    $body = @{
        key = $Key
        values = $values
    } | ConvertTo-Json -Depth 10
    
    try {
        # Vérifier si la variable existe déjà
        $existing = Get-ExistingVariables | Where-Object { $_.key -eq $Key }
        
        if ($existing -and -not $Force) {
            Write-Warning "  Variable $Key existe déjà"
            Write-Info "  Utilisez -Force pour la mettre à jour"
            return $false
        }
        
        # Si existe et Force, supprimer d'abord
        if ($existing -and $Force) {
            Write-Info "  Suppression de l'ancienne variable..."
            try {
                Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env/$($existing.id)" -Method Delete -Headers $headers | Out-Null
                Write-Success "  ✅ Ancienne variable supprimée"
            } catch {
                Write-Warning "  Impossible de supprimer l'ancienne variable (peut-être déjà supprimée)"
            }
        }
        
        # Créer la nouvelle variable
        Write-Info "  Création de la variable..."
        $response = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID/env" -Method Post -Headers $headers -Body $body
        
        Write-Success "  ✅ Variable $Key configurée avec succès"
        return $true
        
    } catch {
        $errorDetails = $_.ErrorDetails.Message
        if ($errorDetails) {
            try {
                $errorJson = $errorDetails | ConvertFrom-Json
                if ($errorJson.message) {
                    Write-Error "  ❌ Erreur: $($errorJson.message)"
                } else {
                    Write-Error "  ❌ Erreur: $errorDetails"
                }
            } catch {
                Write-Error "  ❌ Erreur: $errorDetails"
            }
        } else {
            Write-Error "  ❌ Erreur: $_"
        }
        return $false
    }
}

# Vérifier le token
Write-Info "`nVérification du token..."
try {
    $user = Invoke-RestMethod -Uri "$API_BASE/user" -Method Get -Headers $headers
    Write-Success "✅ Token valide - Connecté en tant que: $($user.email)"
} catch {
    Write-Error "❌ Token invalide ou expiré"
    Write-Info "💡 Obtenez un nouveau token sur: https://app.netlify.com/user/applications"
    exit 1
}

# Vérifier l'accès au site
Write-Info "`nVérification de l'accès au site..."
try {
    $site = Invoke-RestMethod -Uri "$API_BASE/sites/$SITE_ID" -Method Get -Headers $headers
    Write-Success "✅ Accès au site confirmé: $($site.name)"
    Write-Info "   URL: $($site.url)"
} catch {
    Write-Error "❌ Impossible d'accéder au site. Vérifiez le SITE_ID et les permissions du token"
    exit 1
}

# Lister les variables existantes
Write-Info "`nVariables existantes:"
$existingVars = Get-ExistingVariables
if ($existingVars) {
    foreach ($var in $existingVars) {
        $contextsStr = ($var.values | ForEach-Object { $_.context }) -join ", "
        Write-Host "  - $($var.key) [$contextsStr]" -ForegroundColor Gray
    }
} else {
    Write-Info "  Aucune variable configurée"
}

# Configurer chaque variable
Write-Info "`nConfiguration des variables..."
$successCount = 0
$failCount = 0

foreach ($varName in $variables.Keys) {
    $varValue = $variables[$varName]
    $success = Set-NetlifyVariable -Key $varName -Value $varValue -Contexts $contexts
    if ($success) {
        $successCount++
    } else {
        $failCount++
    }
}

# Résumé
Write-Info "`n=== Résumé ==="
Write-Success "✅ Variables configurées avec succès: $successCount"
if ($failCount -gt 0) {
    Write-Warning "⚠️ Variables en échec: $failCount"
}

# Vérification finale
Write-Info "`nVérification finale:"
$finalVars = Get-ExistingVariables
$configuredVars = @()
foreach ($varName in $variables.Keys) {
    $found = $finalVars | Where-Object { $_.key -eq $varName }
    if ($found) {
        $configuredVars += $varName
        Write-Success "  ✅ $varName configurée"
    } else {
        Write-Warning "  ⚠️ $varName non trouvée"
    }
}

Write-Info "`n=== Configuration terminée ==="
Write-Info "💡 Redéployez le site dans Netlify Dashboard pour appliquer les changements"
Write-Info "   URL: https://app.netlify.com/projects/$SITE_ID/deploys"



