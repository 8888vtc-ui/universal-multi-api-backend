# Script PowerShell pour déployer sur Fly.io
# Usage: .\deploy_flyio.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Déploiement Universal API Hub sur Fly.io" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier que Fly CLI est installé
Write-Host "[1/6] Vérification Fly CLI..." -ForegroundColor Yellow
try {
    $flyVersion = fly version 2>&1
    Write-Host "✅ Fly CLI installé: $flyVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Fly CLI non installé!" -ForegroundColor Red
    Write-Host "Installez-le avec: iwr https://fly.io/install.ps1 -useb | iex" -ForegroundColor Yellow
    exit 1
}

# Vérifier la connexion
Write-Host "[2/6] Vérification connexion Fly.io..." -ForegroundColor Yellow
try {
    $whoami = fly auth whoami 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Non connecté. Connexion..." -ForegroundColor Yellow
        fly auth login
    } else {
        Write-Host "✅ Connecté: $whoami" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Erreur de connexion" -ForegroundColor Red
    exit 1
}

# Aller dans le dossier backend
Write-Host "[3/6] Navigation vers backend..." -ForegroundColor Yellow
$backendPath = Join-Path $PSScriptRoot ".."
Set-Location $backendPath
Write-Host "✅ Dossier: $(Get-Location)" -ForegroundColor Green

# Vérifier que fly.toml existe
if (-not (Test-Path "fly.toml")) {
    Write-Host "⚠️  fly.toml non trouvé. Initialisation..." -ForegroundColor Yellow
    fly launch --no-deploy
}

# Générer JWT_SECRET si pas déjà défini
Write-Host "[4/6] Configuration des secrets..." -ForegroundColor Yellow
$secrets = fly secrets list 2>&1
if ($secrets -notmatch "JWT_SECRET_KEY") {
    Write-Host "Génération JWT_SECRET_KEY..." -ForegroundColor Yellow
    $jwtSecret = python -c "import secrets; print(secrets.token_urlsafe(64))"
    fly secrets set JWT_SECRET_KEY=$jwtSecret
    Write-Host "✅ JWT_SECRET_KEY configuré" -ForegroundColor Green
} else {
    Write-Host "✅ JWT_SECRET_KEY déjà configuré" -ForegroundColor Green
}

# Configuration de base
Write-Host "Configuration variables de base..." -ForegroundColor Yellow
fly secrets set ENVIRONMENT=production
fly secrets set API_HOST=0.0.0.0
fly secrets set API_PORT=8000
Write-Host "✅ Variables de base configurées" -ForegroundColor Green

Write-Host ""
Write-Host "⚠️  IMPORTANT: Ajoutez vos clés API avec:" -ForegroundColor Yellow
Write-Host "   fly secrets set GROQ_API_KEY=votre_cle" -ForegroundColor Cyan
Write-Host "   fly secrets set MISTRAL_API_KEY=votre_cle" -ForegroundColor Cyan
Write-Host "   ... (voir DEPLOIEMENT_FLY_IO.md)" -ForegroundColor Cyan
Write-Host ""

# Demander confirmation
$confirm = Read-Host "Continuer le déploiement? (O/N)"
if ($confirm -ne "O" -and $confirm -ne "o") {
    Write-Host "Déploiement annulé." -ForegroundColor Yellow
    exit 0
}

# Déployer
Write-Host "[5/6] Déploiement en cours..." -ForegroundColor Yellow
Write-Host "Cela peut prendre 3-5 minutes..." -ForegroundColor Cyan
fly deploy

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[6/6] Vérification du déploiement..." -ForegroundColor Yellow
    
    # Obtenir l'URL
    $status = fly status
    $url = ($status | Select-String "Hostname").ToString().Split(":")[1].Trim()
    
    Write-Host ""
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "  ✅ Déploiement réussi!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 URL de votre API:" -ForegroundColor Cyan
    Write-Host "   https://$url" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Endpoints:" -ForegroundColor Cyan
    Write-Host "   Health: https://$url/api/health" -ForegroundColor White
    Write-Host "   Docs:   https://$url/docs" -ForegroundColor White
    Write-Host ""
    Write-Host "📊 Commandes utiles:" -ForegroundColor Cyan
    Write-Host "   fly status      - Voir le statut" -ForegroundColor White
    Write-Host "   fly logs        - Voir les logs" -ForegroundColor White
    Write-Host "   fly secrets list - Voir les secrets" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "❌ Erreur lors du déploiement" -ForegroundColor Red
    Write-Host "Voir les logs: fly logs" -ForegroundColor Yellow
    exit 1
}





