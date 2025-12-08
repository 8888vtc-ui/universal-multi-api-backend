# deploy-simple.ps1
# Script de deploiement simplifie sans emojis

param(
    [switch]$Backend = $true,
    [switch]$Frontend = $true
)

$ErrorActionPreference = "Continue"

$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"
$FLY_APP = "universal-api-hub"
$BACKEND_URL = "https://$FLY_APP.fly.dev"
$NETLIFY_SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$NETLIFY_SITE_NAME = "incomparable-semolina-c3a66d"

function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "Deploiement en cours..."

# Deploiement Backend
if ($Backend) {
    Write-Info "`nDeploiement Backend (Fly.io)..."
    
    Push-Location $BACKEND_DIR
    try {
        # Verifier Fly CLI
        $null = fly version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Fly CLI non installe"
            Pop-Location
            exit 1
        }
        
        # Deployer
        Write-Info "Deploiement en cours..."
        fly deploy --remote-only
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Backend deploye avec succes!"
            Write-Info "URL: $BACKEND_URL"
        } else {
            Write-Error "Erreur lors du deploiement backend"
            Pop-Location
            exit 1
        }
    } catch {
        Write-Error "Erreur: $_"
        Pop-Location
        exit 1
    } finally {
        Pop-Location
    }
}

# Deploiement Frontend
if ($Frontend) {
    Write-Info "`nDeploiement Frontend (Netlify via Git)..."
    
    Push-Location $FRONTEND_DIR
    try {
        # Verifier les changements
        $gitStatus = git status --porcelain 2>&1
        
        if ($gitStatus) {
            Write-Info "Changements detectes, commit et push..."
            git add . 2>&1 | Out-Null
            $commitMessage = "Auto-deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git commit -m $commitMessage 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Info "Push sur Git..."
                git push origin main 2>&1 | Out-Null
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Frontend pousse sur Git. Netlify deployera automatiquement."
                } else {
                    Write-Error "Erreur lors du push Git"
                    Pop-Location
                    exit 1
                }
            } else {
                Write-Warning "Aucun changement a committer"
            }
        } else {
            Write-Warning "Aucun changement detecte"
        }
    } catch {
        Write-Error "Erreur: $_"
        Pop-Location
        exit 1
    } finally {
        Pop-Location
    }
}

Write-Success "`nDeploiement termine!"



param(
    [switch]$Backend = $true,
    [switch]$Frontend = $true
)

$ErrorActionPreference = "Continue"

$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"
$FLY_APP = "universal-api-hub"
$BACKEND_URL = "https://$FLY_APP.fly.dev"
$NETLIFY_SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$NETLIFY_SITE_NAME = "incomparable-semolina-c3a66d"

function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }

Write-Info "Deploiement en cours..."

# Deploiement Backend
if ($Backend) {
    Write-Info "`nDeploiement Backend (Fly.io)..."
    
    Push-Location $BACKEND_DIR
    try {
        # Verifier Fly CLI
        $null = fly version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Fly CLI non installe"
            Pop-Location
            exit 1
        }
        
        # Deployer
        Write-Info "Deploiement en cours..."
        fly deploy --remote-only
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Backend deploye avec succes!"
            Write-Info "URL: $BACKEND_URL"
        } else {
            Write-Error "Erreur lors du deploiement backend"
            Pop-Location
            exit 1
        }
    } catch {
        Write-Error "Erreur: $_"
        Pop-Location
        exit 1
    } finally {
        Pop-Location
    }
}

# Deploiement Frontend
if ($Frontend) {
    Write-Info "`nDeploiement Frontend (Netlify via Git)..."
    
    Push-Location $FRONTEND_DIR
    try {
        # Verifier les changements
        $gitStatus = git status --porcelain 2>&1
        
        if ($gitStatus) {
            Write-Info "Changements detectes, commit et push..."
            git add . 2>&1 | Out-Null
            $commitMessage = "Auto-deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git commit -m $commitMessage 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Info "Push sur Git..."
                git push origin main 2>&1 | Out-Null
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "Frontend pousse sur Git. Netlify deployera automatiquement."
                } else {
                    Write-Error "Erreur lors du push Git"
                    Pop-Location
                    exit 1
                }
            } else {
                Write-Warning "Aucun changement a committer"
            }
        } else {
            Write-Warning "Aucun changement detecte"
        }
    } catch {
        Write-Error "Erreur: $_"
        Pop-Location
        exit 1
    } finally {
        Pop-Location
    }
}

Write-Success "`nDeploiement termine!"

