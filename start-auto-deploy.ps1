# start-auto-deploy.ps1
# Script de démarrage rapide pour auto-deploy

Write-Host "🚀 Démarrage du déploiement automatique" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Vérifier que auto-deploy.ps1 existe
if (-not (Test-Path "auto-deploy.ps1")) {
    Write-Host "❌ Fichier auto-deploy.ps1 non trouvé!" -ForegroundColor Red
    exit 1
}

# Menu de sélection
Write-Host "`nChoisissez un mode:" -ForegroundColor Yellow
Write-Host "1. Surveillance automatique (recommandé)" -ForegroundColor White
Write-Host "2. Déploiement unique (tout)" -ForegroundColor White
Write-Host "3. Déploiement unique (backend uniquement)" -ForegroundColor White
Write-Host "4. Déploiement unique (frontend uniquement)" -ForegroundColor White
Write-Host "5. Test des prérequis" -ForegroundColor White
Write-Host "6. Quitter" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Votre choix (1-6)"

switch ($choice) {
    "1" {
        Write-Host "`n👀 Démarrage de la surveillance..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1" -Watch
    }
    "2" {
        Write-Host "`n📦 Déploiement unique (tout)..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1"
    }
    "3" {
        Write-Host "`n📦 Déploiement unique (backend)..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1" -Backend
    }
    "4" {
        Write-Host "`n📦 Déploiement unique (frontend)..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1" -Frontend
    }
    "5" {
        Write-Host "`n🧪 Test des prérequis..." -ForegroundColor Cyan
        & ".\test-auto-deploy.ps1"
    }
    "6" {
        Write-Host "Au revoir!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "❌ Choix invalide!" -ForegroundColor Red
        exit 1
    }
}


# Script de démarrage rapide pour auto-deploy

Write-Host "🚀 Démarrage du déploiement automatique" -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Vérifier que auto-deploy.ps1 existe
if (-not (Test-Path "auto-deploy.ps1")) {
    Write-Host "❌ Fichier auto-deploy.ps1 non trouvé!" -ForegroundColor Red
    exit 1
}

# Menu de sélection
Write-Host "`nChoisissez un mode:" -ForegroundColor Yellow
Write-Host "1. Surveillance automatique (recommandé)" -ForegroundColor White
Write-Host "2. Déploiement unique (tout)" -ForegroundColor White
Write-Host "3. Déploiement unique (backend uniquement)" -ForegroundColor White
Write-Host "4. Déploiement unique (frontend uniquement)" -ForegroundColor White
Write-Host "5. Test des prérequis" -ForegroundColor White
Write-Host "6. Quitter" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Votre choix (1-6)"

switch ($choice) {
    "1" {
        Write-Host "`n👀 Démarrage de la surveillance..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1" -Watch
    }
    "2" {
        Write-Host "`n📦 Déploiement unique (tout)..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1"
    }
    "3" {
        Write-Host "`n📦 Déploiement unique (backend)..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1" -Backend
    }
    "4" {
        Write-Host "`n📦 Déploiement unique (frontend)..." -ForegroundColor Cyan
        & ".\auto-deploy.ps1" -Frontend
    }
    "5" {
        Write-Host "`n🧪 Test des prérequis..." -ForegroundColor Cyan
        & ".\test-auto-deploy.ps1"
    }
    "6" {
        Write-Host "Au revoir!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "❌ Choix invalide!" -ForegroundColor Red
        exit 1
    }
}



