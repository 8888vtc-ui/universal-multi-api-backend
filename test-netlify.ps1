# test-netlify.ps1
# Script de diagnostic Netlify

Write-Host "=== Diagnostic Netlify ===" -ForegroundColor Cyan
Write-Host ""

# 1. Vérifier installation
Write-Host "1. Verification installation..." -ForegroundColor Yellow
$netlify = Get-Command netlify -ErrorAction SilentlyContinue
if ($netlify) {
    Write-Host "   [OK] Netlify CLI installe: $($netlify.Source)" -ForegroundColor Green
    $version = npm list -g netlify-cli 2>&1 | Select-String "netlify-cli@"
    if ($version) {
        Write-Host "   Version: $version" -ForegroundColor Gray
    }
} else {
    Write-Host "   [ERREUR] Netlify CLI non installe" -ForegroundColor Red
    Write-Host "   Installez avec: npm install -g netlify-cli" -ForegroundColor Yellow
    exit 1
}

# 2. Vérifier authentification (avec timeout)
Write-Host "`n2. Verification authentification..." -ForegroundColor Yellow
try {
    $job = Start-Job -ScriptBlock { netlify whoami 2>&1 }
    $result = Wait-Job $job -Timeout 10
    if ($result.State -eq "Completed") {
        $output = Receive-Job $job
        if ($output -match "Logged in as|You are logged in") {
            Write-Host "   [OK] Authentifie" -ForegroundColor Green
            Write-Host "   $output" -ForegroundColor Gray
        } else {
            Write-Host "   [ERREUR] Non authentifie" -ForegroundColor Red
            Write-Host "   Connectez-vous avec: netlify login" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   [TIMEOUT] La commande prend trop de temps" -ForegroundColor Red
        Write-Host "   Possible probleme de reseau ou authentification expiree" -ForegroundColor Yellow
        Write-Host "   Solution: netlify logout; netlify login" -ForegroundColor Cyan
    }
    Remove-Job $job -Force
} catch {
    Write-Host "   [ERREUR] Impossible de verifier: $_" -ForegroundColor Red
}

# 3. Vérifier projet lié
Write-Host "`n3. Verification projet lie..." -ForegroundColor Yellow
if (Test-Path "frontend\.netlify") {
    Write-Host "   [OK] Dossier .netlify existe" -ForegroundColor Green
    try {
        Push-Location frontend
        $job = Start-Job -ScriptBlock { netlify status 2>&1 }
        $result = Wait-Job $job -Timeout 10
        if ($result.State -eq "Completed") {
            $output = Receive-Job $job
            if ($output -match "Project already linked|incomparable-semolina") {
                Write-Host "   [OK] Projet lie" -ForegroundColor Green
                Write-Host "   $($output -split "`n" | Select-Object -First 3)" -ForegroundColor Gray
            } else {
                Write-Host "   [ATTENTION] Projet peut-etre non lie correctement" -ForegroundColor Yellow
            }
        } else {
            Write-Host "   [TIMEOUT] Impossible de verifier le statut" -ForegroundColor Red
        }
        Remove-Job $job -Force
        Pop-Location
    } catch {
        Write-Host "   [ERREUR] $_" -ForegroundColor Red
        Pop-Location
    }
} else {
    Write-Host "   [ATTENTION] Dossier .netlify non trouve" -ForegroundColor Yellow
    Write-Host "   Liez avec: cd frontend; netlify link --id 2d6f74c0-6884-479f-9d56-19b6003a9b08" -ForegroundColor Cyan
}

# 4. Test commande simple
Write-Host "`n4. Test commande env:list (timeout 15s)..." -ForegroundColor Yellow
try {
    Push-Location frontend
    $job = Start-Job -ScriptBlock { netlify env:list 2>&1 }
    $result = Wait-Job $job -Timeout 15
    if ($result.State -eq "Completed") {
        $output = Receive-Job $job
        Write-Host "   [OK] Commande fonctionne" -ForegroundColor Green
        $lines = $output -split "`n" | Select-Object -First 10
        foreach ($line in $lines) {
            if ($line.Trim()) {
                Write-Host "   $line" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "   [TIMEOUT] Commande bloque (plus de 15s)" -ForegroundColor Red
        Write-Host "   La CLI Netlify semble avoir des problemes" -ForegroundColor Yellow
        Write-Host "   Solution: Utiliser le Dashboard Netlify" -ForegroundColor Cyan
    }
    Remove-Job $job -Force
    Pop-Location
} catch {
    Write-Host "   [ERREUR] $_" -ForegroundColor Red
    Pop-Location
}

Write-Host "`n=== Fin du diagnostic ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Recommandation:" -ForegroundColor Yellow
Write-Host "  Si les commandes sont bloquees, utilisez le Dashboard:" -ForegroundColor White
Write-Host "  https://app.netlify.com/projects/incomparable-semolina-c3a66d/settings/env" -ForegroundColor Cyan


# Script de diagnostic Netlify

Write-Host "=== Diagnostic Netlify ===" -ForegroundColor Cyan
Write-Host ""

# 1. Vérifier installation
Write-Host "1. Verification installation..." -ForegroundColor Yellow
$netlify = Get-Command netlify -ErrorAction SilentlyContinue
if ($netlify) {
    Write-Host "   [OK] Netlify CLI installe: $($netlify.Source)" -ForegroundColor Green
    $version = npm list -g netlify-cli 2>&1 | Select-String "netlify-cli@"
    if ($version) {
        Write-Host "   Version: $version" -ForegroundColor Gray
    }
} else {
    Write-Host "   [ERREUR] Netlify CLI non installe" -ForegroundColor Red
    Write-Host "   Installez avec: npm install -g netlify-cli" -ForegroundColor Yellow
    exit 1
}

# 2. Vérifier authentification (avec timeout)
Write-Host "`n2. Verification authentification..." -ForegroundColor Yellow
try {
    $job = Start-Job -ScriptBlock { netlify whoami 2>&1 }
    $result = Wait-Job $job -Timeout 10
    if ($result.State -eq "Completed") {
        $output = Receive-Job $job
        if ($output -match "Logged in as|You are logged in") {
            Write-Host "   [OK] Authentifie" -ForegroundColor Green
            Write-Host "   $output" -ForegroundColor Gray
        } else {
            Write-Host "   [ERREUR] Non authentifie" -ForegroundColor Red
            Write-Host "   Connectez-vous avec: netlify login" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   [TIMEOUT] La commande prend trop de temps" -ForegroundColor Red
        Write-Host "   Possible probleme de reseau ou authentification expiree" -ForegroundColor Yellow
        Write-Host "   Solution: netlify logout; netlify login" -ForegroundColor Cyan
    }
    Remove-Job $job -Force
} catch {
    Write-Host "   [ERREUR] Impossible de verifier: $_" -ForegroundColor Red
}

# 3. Vérifier projet lié
Write-Host "`n3. Verification projet lie..." -ForegroundColor Yellow
if (Test-Path "frontend\.netlify") {
    Write-Host "   [OK] Dossier .netlify existe" -ForegroundColor Green
    try {
        Push-Location frontend
        $job = Start-Job -ScriptBlock { netlify status 2>&1 }
        $result = Wait-Job $job -Timeout 10
        if ($result.State -eq "Completed") {
            $output = Receive-Job $job
            if ($output -match "Project already linked|incomparable-semolina") {
                Write-Host "   [OK] Projet lie" -ForegroundColor Green
                Write-Host "   $($output -split "`n" | Select-Object -First 3)" -ForegroundColor Gray
            } else {
                Write-Host "   [ATTENTION] Projet peut-etre non lie correctement" -ForegroundColor Yellow
            }
        } else {
            Write-Host "   [TIMEOUT] Impossible de verifier le statut" -ForegroundColor Red
        }
        Remove-Job $job -Force
        Pop-Location
    } catch {
        Write-Host "   [ERREUR] $_" -ForegroundColor Red
        Pop-Location
    }
} else {
    Write-Host "   [ATTENTION] Dossier .netlify non trouve" -ForegroundColor Yellow
    Write-Host "   Liez avec: cd frontend; netlify link --id 2d6f74c0-6884-479f-9d56-19b6003a9b08" -ForegroundColor Cyan
}

# 4. Test commande simple
Write-Host "`n4. Test commande env:list (timeout 15s)..." -ForegroundColor Yellow
try {
    Push-Location frontend
    $job = Start-Job -ScriptBlock { netlify env:list 2>&1 }
    $result = Wait-Job $job -Timeout 15
    if ($result.State -eq "Completed") {
        $output = Receive-Job $job
        Write-Host "   [OK] Commande fonctionne" -ForegroundColor Green
        $lines = $output -split "`n" | Select-Object -First 10
        foreach ($line in $lines) {
            if ($line.Trim()) {
                Write-Host "   $line" -ForegroundColor Gray
            }
        }
    } else {
        Write-Host "   [TIMEOUT] Commande bloque (plus de 15s)" -ForegroundColor Red
        Write-Host "   La CLI Netlify semble avoir des problemes" -ForegroundColor Yellow
        Write-Host "   Solution: Utiliser le Dashboard Netlify" -ForegroundColor Cyan
    }
    Remove-Job $job -Force
    Pop-Location
} catch {
    Write-Host "   [ERREUR] $_" -ForegroundColor Red
    Pop-Location
}

Write-Host "`n=== Fin du diagnostic ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Recommandation:" -ForegroundColor Yellow
Write-Host "  Si les commandes sont bloquees, utilisez le Dashboard:" -ForegroundColor White
Write-Host "  https://app.netlify.com/projects/incomparable-semolina-c3a66d/settings/env" -ForegroundColor Cyan



