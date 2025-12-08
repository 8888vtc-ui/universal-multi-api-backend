# configure-netlify.ps1
# Script pour configurer les variables d'environnement Netlify

param(
    [switch]$Force = $false
)

$ErrorActionPreference = "Continue"

$FRONTEND_DIR = "frontend"
$BACKEND_URL = "https://universal-api-hub.fly.dev"
$NETLIFY_SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"

function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "Configuration des variables d'environnement Netlify"
Write-Info "===================================================="

# Vérifier Netlify CLI
if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
    Write-Error "Netlify CLI non installé!"
    Write-Info "Installez-le avec: npm install -g netlify-cli"
    exit 1
}

Push-Location $FRONTEND_DIR

try {
    # Vérifier que le projet est lié
    $status = netlify status 2>&1
    if ($status -match "No project id found") {
        Write-Info "Liaison du projet Netlify..."
        netlify link --id $NETLIFY_SITE_ID
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Impossible de lier le projet"
            Pop-Location
            exit 1
        }
    }
    
    Write-Success "Projet lié: $NETLIFY_SITE_ID"
    
    # Variables à configurer
    $variables = @{
        "NEXT_PUBLIC_API_URL" = $BACKEND_URL
        "NEXT_PUBLIC_APP_NAME" = "WikiAsk"
        "NEXT_PUBLIC_APP_SLOGAN" = "Ask Everything. Know Everything."
    }
    
    # Contextes Netlify
    $contexts = @("production", "deploy-preview", "branch-deploy")
    
    # Lister les variables existantes
    Write-Info "`nVariables existantes:"
    $envList = netlify env:list 2>&1
    Write-Host $envList
    
    # Configurer chaque variable pour chaque contexte
    foreach ($varName in $variables.Keys) {
        $varValue = $variables[$varName]
        
        Write-Info "`nConfiguration de $varName = $varValue"
        
        foreach ($context in $contexts) {
            Write-Info "  → Contexte: $context"
            
            if ($Force) {
                # Forcer la mise à jour
                $result = netlify env:set $varName $varValue --context $context 2>&1
            } else {
                # Vérifier si la variable existe déjà
                if ($envList -match "$varName.*$context") {
                    Write-Warning "    Variable déjà définie pour $context, utilisation de --force pour mettre à jour"
                    $result = netlify env:set $varName $varValue --context $context --force 2>&1
                } else {
                    $result = netlify env:set $varName $varValue --context $context 2>&1
                }
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "    ✅ Configuré pour $context"
            } else {
                Write-Warning "    ⚠️ Erreur: $result"
            }
        }
    }
    
    Write-Info "`nVérification finale:"
    $finalList = netlify env:list 2>&1
    Write-Host $finalList
    
    Write-Success "`n✅ Configuration terminée!"
    Write-Info "💡 Redéployez le site dans Netlify Dashboard pour appliquer les changements"
    
} catch {
    Write-Error "Erreur: $_"
    Pop-Location
    exit 1
} finally {
    Pop-Location
}


# Script pour configurer les variables d'environnement Netlify

param(
    [switch]$Force = $false
)

$ErrorActionPreference = "Continue"

$FRONTEND_DIR = "frontend"
$BACKEND_URL = "https://universal-api-hub.fly.dev"
$NETLIFY_SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"

function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "Configuration des variables d'environnement Netlify"
Write-Info "===================================================="

# Vérifier Netlify CLI
if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
    Write-Error "Netlify CLI non installé!"
    Write-Info "Installez-le avec: npm install -g netlify-cli"
    exit 1
}

Push-Location $FRONTEND_DIR

try {
    # Vérifier que le projet est lié
    $status = netlify status 2>&1
    if ($status -match "No project id found") {
        Write-Info "Liaison du projet Netlify..."
        netlify link --id $NETLIFY_SITE_ID
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Impossible de lier le projet"
            Pop-Location
            exit 1
        }
    }
    
    Write-Success "Projet lié: $NETLIFY_SITE_ID"
    
    # Variables à configurer
    $variables = @{
        "NEXT_PUBLIC_API_URL" = $BACKEND_URL
        "NEXT_PUBLIC_APP_NAME" = "WikiAsk"
        "NEXT_PUBLIC_APP_SLOGAN" = "Ask Everything. Know Everything."
    }
    
    # Contextes Netlify
    $contexts = @("production", "deploy-preview", "branch-deploy")
    
    # Lister les variables existantes
    Write-Info "`nVariables existantes:"
    $envList = netlify env:list 2>&1
    Write-Host $envList
    
    # Configurer chaque variable pour chaque contexte
    foreach ($varName in $variables.Keys) {
        $varValue = $variables[$varName]
        
        Write-Info "`nConfiguration de $varName = $varValue"
        
        foreach ($context in $contexts) {
            Write-Info "  → Contexte: $context"
            
            if ($Force) {
                # Forcer la mise à jour
                $result = netlify env:set $varName $varValue --context $context 2>&1
            } else {
                # Vérifier si la variable existe déjà
                if ($envList -match "$varName.*$context") {
                    Write-Warning "    Variable déjà définie pour $context, utilisation de --force pour mettre à jour"
                    $result = netlify env:set $varName $varValue --context $context --force 2>&1
                } else {
                    $result = netlify env:set $varName $varValue --context $context 2>&1
                }
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Success "    ✅ Configuré pour $context"
            } else {
                Write-Warning "    ⚠️ Erreur: $result"
            }
        }
    }
    
    Write-Info "`nVérification finale:"
    $finalList = netlify env:list 2>&1
    Write-Host $finalList
    
    Write-Success "`n✅ Configuration terminée!"
    Write-Info "💡 Redéployez le site dans Netlify Dashboard pour appliquer les changements"
    
} catch {
    Write-Error "Erreur: $_"
    Pop-Location
    exit 1
} finally {
    Pop-Location
}



