# test-auto-deploy.ps1
# Script de test pour vérifier que auto-deploy.ps1 fonctionne

Write-Host "🧪 Test du script auto-deploy.ps1" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Test 1: Vérifier que le fichier existe
Write-Host "`n[1/5] Vérification du fichier..." -ForegroundColor Yellow
if (Test-Path "auto-deploy.ps1") {
    Write-Host "✅ Fichier auto-deploy.ps1 trouvé" -ForegroundColor Green
} else {
    Write-Host "❌ Fichier auto-deploy.ps1 non trouvé" -ForegroundColor Red
    exit 1
}

# Test 2: Vérifier la syntaxe PowerShell
Write-Host "`n[2/5] Vérification de la syntaxe..." -ForegroundColor Yellow
try {
    $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content "auto-deploy.ps1" -Raw), [ref]$null)
    Write-Host "✅ Syntaxe PowerShell valide" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur de syntaxe: $_" -ForegroundColor Red
    exit 1
}

# Test 3: Vérifier les prérequis backend
Write-Host "`n[3/5] Vérification prérequis backend (Fly.io)..." -ForegroundColor Yellow
try {
    $flyVersion = fly version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Fly CLI installé: $($flyVersion[0])" -ForegroundColor Green
        
        # Vérifier la connexion
        fly auth whoami 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Connecté à Fly.io" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Non connecté à Fly.io (exécutez: fly auth login)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ Fly CLI non installé" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Fly CLI non disponible" -ForegroundColor Yellow
}

# Test 4: Vérifier les prérequis frontend
Write-Host "`n[4/5] Vérification prérequis frontend (Git)..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Git installé: $gitVersion" -ForegroundColor Green
        
        # Vérifier le remote
        $remote = git remote get-url origin 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Remote Git configuré: $remote" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Remote Git non configuré" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ Git non installé" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Git non disponible" -ForegroundColor Yellow
}

# Test 5: Vérifier la structure du projet
Write-Host "`n[5/5] Vérification structure du projet..." -ForegroundColor Yellow
if (Test-Path "backend") {
    Write-Host "✅ Dossier backend trouvé" -ForegroundColor Green
} else {
    Write-Host "❌ Dossier backend non trouvé" -ForegroundColor Red
}

if (Test-Path "frontend") {
    Write-Host "✅ Dossier frontend trouvé" -ForegroundColor Green
} else {
    Write-Host "❌ Dossier frontend non trouvé" -ForegroundColor Red
}

Write-Host "`n✅ Tests terminés!" -ForegroundColor Green
Write-Host "`n💡 Pour démarrer la surveillance:" -ForegroundColor Cyan
Write-Host "   .\auto-deploy.ps1 -Watch" -ForegroundColor White


# Script de test pour vérifier que auto-deploy.ps1 fonctionne

Write-Host "🧪 Test du script auto-deploy.ps1" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

# Test 1: Vérifier que le fichier existe
Write-Host "`n[1/5] Vérification du fichier..." -ForegroundColor Yellow
if (Test-Path "auto-deploy.ps1") {
    Write-Host "✅ Fichier auto-deploy.ps1 trouvé" -ForegroundColor Green
} else {
    Write-Host "❌ Fichier auto-deploy.ps1 non trouvé" -ForegroundColor Red
    exit 1
}

# Test 2: Vérifier la syntaxe PowerShell
Write-Host "`n[2/5] Vérification de la syntaxe..." -ForegroundColor Yellow
try {
    $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content "auto-deploy.ps1" -Raw), [ref]$null)
    Write-Host "✅ Syntaxe PowerShell valide" -ForegroundColor Green
} catch {
    Write-Host "❌ Erreur de syntaxe: $_" -ForegroundColor Red
    exit 1
}

# Test 3: Vérifier les prérequis backend
Write-Host "`n[3/5] Vérification prérequis backend (Fly.io)..." -ForegroundColor Yellow
try {
    $flyVersion = fly version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Fly CLI installé: $($flyVersion[0])" -ForegroundColor Green
        
        # Vérifier la connexion
        fly auth whoami 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Connecté à Fly.io" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Non connecté à Fly.io (exécutez: fly auth login)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ Fly CLI non installé" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Fly CLI non disponible" -ForegroundColor Yellow
}

# Test 4: Vérifier les prérequis frontend
Write-Host "`n[4/5] Vérification prérequis frontend (Git)..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Git installé: $gitVersion" -ForegroundColor Green
        
        # Vérifier le remote
        $remote = git remote get-url origin 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Remote Git configuré: $remote" -ForegroundColor Green
        } else {
            Write-Host "⚠️ Remote Git non configuré" -ForegroundColor Yellow
        }
    } else {
        Write-Host "⚠️ Git non installé" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️ Git non disponible" -ForegroundColor Yellow
}

# Test 5: Vérifier la structure du projet
Write-Host "`n[5/5] Vérification structure du projet..." -ForegroundColor Yellow
if (Test-Path "backend") {
    Write-Host "✅ Dossier backend trouvé" -ForegroundColor Green
} else {
    Write-Host "❌ Dossier backend non trouvé" -ForegroundColor Red
}

if (Test-Path "frontend") {
    Write-Host "✅ Dossier frontend trouvé" -ForegroundColor Green
} else {
    Write-Host "❌ Dossier frontend non trouvé" -ForegroundColor Red
}

Write-Host "`n✅ Tests terminés!" -ForegroundColor Green
Write-Host "`n💡 Pour démarrer la surveillance:" -ForegroundColor Cyan
Write-Host "   .\auto-deploy.ps1 -Watch" -ForegroundColor White



