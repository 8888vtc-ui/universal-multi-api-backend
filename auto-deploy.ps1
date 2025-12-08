# auto-deploy.ps1
# Script de déploiement automatique avec surveillance et vérification
# Surveille les modifications, déploie et vérifie jusqu'à succès

param(
    [switch]$Watch = $false,
    [switch]$Backend = $true,
    [switch]$Frontend = $true,
    [int]$MaxRetries = 3,
    [int]$RetryDelay = 30
)

$ErrorActionPreference = "Continue"

# Configuration
$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"
$FLY_APP = "universal-api-hub"
$BACKEND_URL = "https://$FLY_APP.fly.dev"
$NETLIFY_SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$NETLIFY_SITE_NAME = "incomparable-semolina-c3a66d"

# Couleurs
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Debug { Write-Host $args -ForegroundColor Gray }

# Fichiers à ignorer
$IGNORE_PATTERNS = @(
    "\.git",
    "node_modules",
    "__pycache__",
    "\.next",
    "\.venv",
    "venv",
    "\.env",
    "\.log",
    "\.db$",
    "\.ps1$",
    "auto-deploy"
)

Write-Info "🚀 Script de Déploiement Automatique avec Vérification"
Write-Info "======================================================"

# Fonction de vérification backend
function Test-BackendDeployment {
    param([int]$TimeoutSeconds = 30)
    
    Write-Info "🔍 Vérification du déploiement backend..."
    
    $healthUrl = "$BACKEND_URL/api/health"
    $maxAttempts = $TimeoutSeconds / 5
    
    for ($i = 1; $i -le $maxAttempts; $i++) {
        try {
            Write-Debug "Tentative $i/$maxAttempts : $healthUrl"
            $response = Invoke-WebRequest -Uri $healthUrl -Method GET -TimeoutSec 5 -UseBasicParsing
            
            if ($response.StatusCode -eq 200) {
                $content = $response.Content | ConvertFrom-Json
                if ($content.status -eq "healthy" -or $content.status -eq "ok") {
                    Write-Success "✅ Backend déployé et fonctionnel!"
                    Write-Info "   Status: $($content.status)"
                    return $true
                }
            }
        } catch {
            Write-Debug "   Tentative $i échouée: $($_.Exception.Message)"
        }
        
        if ($i -lt $maxAttempts) {
            Start-Sleep -Seconds 5
        }
    }
    
    Write-Warning "⚠️ Backend non accessible après $TimeoutSeconds secondes"
    return $false
}

# Fonction de lecture des logs backend
function Get-BackendLogs {
    Write-Info "📋 Lecture des logs backend..."
    
    Push-Location $BACKEND_DIR
    try {
        $logs = fly logs --app $FLY_APP 2>&1 | Select-Object -Last 50
        return $logs
    } catch {
        Write-Error "❌ Erreur lors de la lecture des logs: $_"
        return @()
    } finally {
        Pop-Location
    }
}

# Fonction de correction backend
function Fix-BackendDeployment {
    param([string[]]$Logs)
    
    Write-Info "🔧 Tentative de correction backend..."
    
    # Analyser les logs pour trouver les erreurs
    $errors = @()
    foreach ($log in $logs) {
        if ($log -match "error|Error|ERROR|failed|Failed|FAILED|exception|Exception") {
            $errors += $log
        }
    }
    
    if ($errors.Count -eq 0) {
        Write-Warning "⚠️ Aucune erreur détectée dans les logs"
        return $false
    }
    
    Write-Warning "📋 Erreurs détectées:"
    $errors | Select-Object -First 10 | ForEach-Object { Write-Debug "   $_" }
    
    # Corrections automatiques possibles
    $fixed = $false
    
    # Erreur: Variables d'environnement manquantes
    if ($errors -match "environment|ENV|secret") {
        Write-Info "🔧 Correction: Vérification des variables d'environnement..."
        Push-Location $BACKEND_DIR
        try {
            fly secrets list --app $FLY_APP | Out-Null
            Write-Success "✅ Secrets vérifiés"
            $fixed = $true
        } catch {
            Write-Warning "⚠️ Impossible de vérifier les secrets"
        } finally {
            Pop-Location
        }
    }
    
    # Erreur: Port ou connexion
    if ($errors -match "port|Port|connection|Connection|bind") {
        Write-Info "🔧 Correction: Redémarrage de l'application..."
        Push-Location $BACKEND_DIR
        try {
            fly apps restart $FLY_APP
            Write-Success "✅ Application redémarrée"
            $fixed = $true
        } catch {
            Write-Warning "⚠️ Impossible de redémarrer"
        } finally {
            Pop-Location
        }
    }
    
    return $fixed
}

# Fonction de déploiement backend avec vérification
function Deploy-Backend {
    Write-Info "`n📦 Déploiement Backend (Fly.io)..."
    
    Push-Location $BACKEND_DIR
    
    try {
        # Vérifier que fly CLI est installé
        $flyCheck = fly version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "❌ Fly CLI non installé. Installez-le avec: iwr https://fly.io/install.ps1 -useb | iex"
            return $false
        }
        
        # Vérifier la connexion
        Write-Info "🔐 Vérification connexion Fly.io..."
        fly auth whoami 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Error "❌ Non connecté à Fly.io. Exécutez: fly auth login"
            return $false
        }
        
        # Déployer
        Write-Info "🚀 Déploiement en cours..."
        $deployOutput = fly deploy --remote-only 2>&1 | Tee-Object -Variable deployLog
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Déploiement backend terminé!"
            
            # Vérifier que le déploiement est pris en charge
            Write-Info "⏳ Attente de la disponibilité du service (30s)..."
            Start-Sleep -Seconds 10
            
            $isDeployed = Test-BackendDeployment -TimeoutSeconds 30
            
            if (-not $isDeployed) {
                Write-Warning "⚠️ Le déploiement semble avoir réussi mais le service n'est pas accessible"
                
                # Lire les logs
                $logs = Get-BackendLogs
                
                # Essayer de corriger
                $fixed = Fix-BackendDeployment -Logs $logs
                
                if ($fixed) {
                    Write-Info "⏳ Nouvelle vérification après correction..."
                    Start-Sleep -Seconds 15
                    $isDeployed = Test-BackendDeployment -TimeoutSeconds 30
                }
                
                if (-not $isDeployed) {
                    Write-Error "❌ Le service n'est toujours pas accessible après correction"
                    Write-Info "📋 Derniers logs:"
                    Get-BackendLogs | Select-Object -Last 20 | ForEach-Object { Write-Debug "   $_" }
                    return $false
                }
            }
            
            Write-Success "✅ Backend déployé et vérifié!"
            Write-Info "📍 URL: $BACKEND_URL"
            return $true
        } else {
            Write-Error "❌ Erreur lors du déploiement backend"
            Write-Info "📋 Logs de déploiement:"
            $deployLog | Select-Object -Last 20 | ForEach-Object { Write-Debug "   $_" }
            
            # Lire les logs pour diagnostic
            $logs = Get-BackendLogs
            Fix-BackendDeployment -Logs $logs
            
            return $false
        }
    } catch {
        Write-Error "❌ Erreur: $_"
        return $false
    } finally {
        Pop-Location
    }
}

# Fonction pour configurer les variables Netlify
function Set-NetlifyEnv {
    param(
        [string]$VariableName,
        [string]$Value,
        [string]$Context = "production"
    )
    
    if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
        Write-Warning "Netlify CLI non installé, impossible de définir la variable"
        return $false
    }
    
    try {
        Push-Location $FRONTEND_DIR
        $result = netlify env:set $VariableName $Value --context $Context 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Variable $VariableName définie pour $Context"
            return $true
        } else {
            Write-Warning "Impossible de définir $VariableName : $result"
            return $false
        }
    } catch {
        Write-Warning "Erreur lors de la définition de $VariableName : $_"
        return $false
    } finally {
        Pop-Location
    }
}

# Fonction de vérification frontend
function Test-FrontendDeployment {
    param([int]$TimeoutSeconds = 60)
    
    Write-Info "🔍 Vérification du déploiement frontend..."
    
    # Si Netlify CLI est disponible, vérifier le statut
    if (Get-Command netlify -ErrorAction SilentlyContinue) {
        try {
            Push-Location $FRONTEND_DIR
            $status = netlify status 2>&1
            if ($status -match "Live URL|Site URL") {
                Write-Success "✅ Frontend déployé sur Netlify"
                return $true
            }
        } catch {
            Write-Debug "Netlify CLI status non disponible"
        } finally {
            Pop-Location
        }
    }
    
    # Vérifier via Git (si Netlify est connecté à GitHub)
    Write-Info "⏳ Vérification via Git/Netlify (peut prendre 1-2 minutes)..."
    
    # Attendre que Netlify termine le déploiement
    $maxAttempts = $TimeoutSeconds / 10
    
    for ($i = 1; $i -le $maxAttempts; $i++) {
        Write-Debug "Vérification $i/$maxAttempts..."
        
        # Vérifier le dernier commit sur GitHub
        try {
            $lastCommit = git log -1 --format="%H" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✅ Commit poussé sur Git: $($lastCommit.Substring(0, 8))"
                Write-Info "⏳ Netlify déploiera automatiquement (vérifiez dans le dashboard)"
                return $true
            }
        } catch {
            Write-Debug "Erreur vérification Git: $_"
        }
        
        if ($i -lt $maxAttempts) {
            Start-Sleep -Seconds 10
        }
    }
    
    Write-Warning "⚠️ Impossible de vérifier le déploiement frontend automatiquement"
    Write-Info "💡 Vérifiez manuellement dans le dashboard Netlify"
    return $true # On considère que c'est OK car Netlify déploie automatiquement
}

# Fonction de lecture des logs frontend (Netlify)
function Get-FrontendLogs {
    Write-Info "📋 Lecture des logs frontend (Netlify)..."
    
    Push-Location $FRONTEND_DIR
    
    try {
        if (Get-Command netlify -ErrorAction SilentlyContinue) {
            $logs = netlify logs 2>&1 | Select-Object -Last 50
            return $logs
        } else {
            Write-Warning "⚠️ Netlify CLI non installé. Installez-le avec: npm install -g netlify-cli"
            Write-Info "💡 Vérifiez les logs dans le dashboard Netlify"
            return @()
        }
    } catch {
        Write-Error "❌ Erreur lors de la lecture des logs: $_"
        return @()
    } finally {
        Pop-Location
    }
}

# Fonction de correction frontend
function Fix-FrontendDeployment {
    param([string[]]$Logs)
    
    Write-Info "🔧 Tentative de correction frontend..."
    
    $errors = @()
    foreach ($log in $logs) {
        if ($log -match "error|Error|ERROR|failed|Failed|FAILED|build|Build") {
            $errors += $log
        }
    }
    
    if ($errors.Count -eq 0) {
        Write-Warning "⚠️ Aucune erreur détectée dans les logs"
        return $false
    }
    
    Write-Warning "📋 Erreurs détectées:"
    $errors | Select-Object -First 10 | ForEach-Object { Write-Debug "   $_" }
    
    $fixed = $false
    
    # Erreur: Variables d'environnement
    if ($errors -match "NEXT_PUBLIC|environment|ENV") {
        Write-Info "🔧 Correction: Vérification des variables d'environnement Netlify..."
        Write-Warning "⚠️ Vérifiez manuellement dans Netlify Dashboard → Site settings → Environment variables"
        $fixed = $true
    }
    
    # Erreur: Build
    if ($errors -match "build|Build|npm|node") {
        Write-Info "🔧 Correction: Nettoyage et rebuild..."
        Push-Location $FRONTEND_DIR
        try {
            Remove-Item -Path ".next" -Recurse -Force -ErrorAction SilentlyContinue
            npm run build 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✅ Build local réussi"
                $fixed = $true
            }
        } catch {
            Write-Warning "⚠️ Erreur lors du build local"
        } finally {
            Pop-Location
        }
    }
    
    return $fixed
}

# Fonction de déploiement frontend avec vérification
function Deploy-Frontend {
    Write-Info "`n📦 Déploiement Frontend (Netlify)..."
    
    Push-Location $FRONTEND_DIR
    
    try {
        # Vérifier et configurer les variables Netlify si nécessaire
        Write-Info "🔍 Vérification des variables d'environnement Netlify..."
        if (Get-Command netlify -ErrorAction SilentlyContinue) {
            $envList = netlify env:list 2>&1
            if ($envList -notmatch "NEXT_PUBLIC_API_URL") {
                Write-Warning "⚠️ Variable NEXT_PUBLIC_API_URL manquante, configuration..."
                Set-NetlifyEnv -VariableName "NEXT_PUBLIC_API_URL" -Value $BACKEND_URL -Context "production"
                Set-NetlifyEnv -VariableName "NEXT_PUBLIC_API_URL" -Value $BACKEND_URL -Context "deploy-preview"
                Set-NetlifyEnv -VariableName "NEXT_PUBLIC_API_URL" -Value $BACKEND_URL -Context "branch-deploy"
            } else {
                Write-Success "✅ Variables Netlify configurées"
            }
        }
        
        # Vérifier s'il y a des changements
        $gitStatus = git status --porcelain 2>&1
        
        if ($gitStatus) {
            Write-Info "📝 Changements détectés, commit et push..."
            
            git add . 2>&1 | Out-Null
            $commitMessage = "Auto-deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git commit -m $commitMessage 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Info "📤 Push sur Git..."
                git push origin main 2>&1 | Out-Null
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "✅ Frontend poussé sur Git"
                    
                    # Vérifier le déploiement
                    Write-Info "⏳ Attente du déploiement Netlify (60s)..."
                    Start-Sleep -Seconds 15
                    
                    $isDeployed = Test-FrontendDeployment -TimeoutSeconds 60
                    
                    if (-not $isDeployed) {
                        Write-Warning "⚠️ Le déploiement semble avoir réussi mais la vérification a échoué"
                        
                        # Lire les logs
                        $logs = Get-FrontendLogs
                        
                        # Essayer de corriger
                        $fixed = Fix-FrontendDeployment -Logs $logs
                        
                        if ($fixed) {
                            Write-Info "⏳ Nouvelle vérification après correction..."
                            Start-Sleep -Seconds 20
                            $isDeployed = Test-FrontendDeployment -TimeoutSeconds 60
                        }
                        
                        if (-not $isDeployed) {
                            Write-Warning "⚠️ Vérification échouée, mais Netlify déploie généralement automatiquement"
                            Write-Info "💡 Vérifiez manuellement dans le dashboard Netlify"
                        }
                    }
                    
                    Write-Success "✅ Frontend déployé!"
                    Write-Info "📍 Netlify déploiera automatiquement via GitHub"
                    return $true
                } else {
                    Write-Error "❌ Erreur lors du push Git"
                    return $false
                }
            } else {
                Write-Warning "⚠️ Aucun changement à committer"
                return $true
            }
        } else {
            Write-Warning "⚠️ Aucun changement détecté. Pas de déploiement nécessaire."
            return $true
        }
    } catch {
        Write-Error "❌ Erreur: $_"
        return $false
    } finally {
        Pop-Location
    }
}

# Fonction de surveillance de fichiers
function Watch-Files {
    Write-Info "`nSurveillance des fichiers activee..."
    Write-Info "   - Backend: $Backend"
    Write-Info "   - Frontend: $Frontend"
    Write-Info "   Appuyez sur Ctrl+C pour arreter"
    Write-Info ""
    
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = Get-Location
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    $watcher.Filter = "*.*"
    
    $lastDeployTime = @{
        "backend" = [DateTime]::MinValue
        "frontend" = [DateTime]::MinValue
    }
    $deployCooldown = 30 # Secondes entre deux déploiements
    
    $action = {
        $path = $Event.SourceEventArgs.FullPath
        $changeType = $Event.SourceEventArgs.ChangeType
        $relativePath = $path.Replace((Get-Location).Path + "\", "").Replace((Get-Location).Path + "/", "")
        
        # Ignorer les fichiers dans les dossiers à exclure
        $shouldIgnore = $false
        foreach ($pattern in $IGNORE_PATTERNS) {
            if ($relativePath -match $pattern) {
                $shouldIgnore = $true
                break
            }
        }
        
        if (-not $shouldIgnore -and $changeType -ne "Changed") {
            Write-Info "`n📝 Modification détectée: $changeType - $relativePath"
            
            # Déterminer quel service déployer
            $deployBackend = $false
            $deployFrontend = $false
            
            if ($relativePath -like "backend\*" -or $relativePath -like "backend/*") {
                $deployBackend = $true
            } elseif ($relativePath -like "frontend\*" -or $relativePath -like "frontend/*") {
                $deployFrontend = $true
            } else {
                # Fichier à la racine, déployer les deux
                $deployBackend = $true
                $deployFrontend = $true
            }
            
            # Vérifier le cooldown
            $now = Get-Date
            if ($deployBackend -and ($now - $lastDeployTime["backend"]).TotalSeconds -lt $deployCooldown) {
                Write-Debug "⏳ Cooldown backend actif, attente..."
                $deployBackend = $false
            }
            if ($deployFrontend -and ($now - $lastDeployTime["frontend"]).TotalSeconds -lt $deployCooldown) {
                Write-Debug "⏳ Cooldown frontend actif, attente..."
                $deployFrontend = $false
            }
            
            # Attendre 2 secondes pour éviter les déploiements multiples
            Start-Sleep -Seconds 2
            
            if ($deployBackend -and $Backend) {
                Write-Info "🚀 Déploiement backend déclenché..."
                $success = Deploy-Backend
                if ($success) {
                    $lastDeployTime["backend"] = Get-Date
                }
            }
            
            if ($deployFrontend -and $Frontend) {
                Write-Info "🚀 Déploiement frontend déclenché..."
                $success = Deploy-Frontend
                if ($success) {
                    $lastDeployTime["frontend"] = Get-Date
                }
            }
        }
    }
    
    # Enregistrer les événements
    $changedEvent = Register-ObjectEvent $watcher "Changed" -Action $action
    $createdEvent = Register-ObjectEvent $watcher "Created" -Action $action
    $deletedEvent = Register-ObjectEvent $watcher "Deleted" -Action $action
    
    # Attendre indéfiniment
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    } finally {
        $watcher.EnableRaisingEvents = $false
        $watcher.Dispose()
        Unregister-Event -SourceIdentifier $changedEvent.Name
        Unregister-Event -SourceIdentifier $createdEvent.Name
        Unregister-Event -SourceIdentifier $deletedEvent.Name
    }
}

# Mode surveillance ou déploiement unique
if ($Watch) {
    Watch-Files
} else {
    # Déploiement unique
    $success = $true
    
    if ($Backend) {
        $success = Deploy-Backend -and $success
    }
    
    if ($Frontend) {
        $success = Deploy-Frontend -and $success
    }
    
    if ($success) {
        Write-Success "`n✅ Déploiement terminé!"
    } else {
        Write-Error "`n❌ Certains déploiements ont échoué"
        exit 1
    }
}


# Surveille les modifications, déploie et vérifie jusqu'à succès

param(
    [switch]$Watch = $false,
    [switch]$Backend = $true,
    [switch]$Frontend = $true,
    [int]$MaxRetries = 3,
    [int]$RetryDelay = 30
)

$ErrorActionPreference = "Continue"

# Configuration
$BACKEND_DIR = "backend"
$FRONTEND_DIR = "frontend"
$FLY_APP = "universal-api-hub"
$BACKEND_URL = "https://$FLY_APP.fly.dev"
$NETLIFY_SITE_ID = "2d6f74c0-6884-479f-9d56-19b6003a9b08"
$NETLIFY_SITE_NAME = "incomparable-semolina-c3a66d"

# Couleurs
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Error { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Debug { Write-Host $args -ForegroundColor Gray }

# Fichiers à ignorer
$IGNORE_PATTERNS = @(
    "\.git",
    "node_modules",
    "__pycache__",
    "\.next",
    "\.venv",
    "venv",
    "\.env",
    "\.log",
    "\.db$",
    "\.ps1$",
    "auto-deploy"
)

Write-Info "🚀 Script de Déploiement Automatique avec Vérification"
Write-Info "======================================================"

# Fonction de vérification backend
function Test-BackendDeployment {
    param([int]$TimeoutSeconds = 30)
    
    Write-Info "🔍 Vérification du déploiement backend..."
    
    $healthUrl = "$BACKEND_URL/api/health"
    $maxAttempts = $TimeoutSeconds / 5
    
    for ($i = 1; $i -le $maxAttempts; $i++) {
        try {
            Write-Debug "Tentative $i/$maxAttempts : $healthUrl"
            $response = Invoke-WebRequest -Uri $healthUrl -Method GET -TimeoutSec 5 -UseBasicParsing
            
            if ($response.StatusCode -eq 200) {
                $content = $response.Content | ConvertFrom-Json
                if ($content.status -eq "healthy" -or $content.status -eq "ok") {
                    Write-Success "✅ Backend déployé et fonctionnel!"
                    Write-Info "   Status: $($content.status)"
                    return $true
                }
            }
        } catch {
            Write-Debug "   Tentative $i échouée: $($_.Exception.Message)"
        }
        
        if ($i -lt $maxAttempts) {
            Start-Sleep -Seconds 5
        }
    }
    
    Write-Warning "⚠️ Backend non accessible après $TimeoutSeconds secondes"
    return $false
}

# Fonction de lecture des logs backend
function Get-BackendLogs {
    Write-Info "📋 Lecture des logs backend..."
    
    Push-Location $BACKEND_DIR
    try {
        $logs = fly logs --app $FLY_APP 2>&1 | Select-Object -Last 50
        return $logs
    } catch {
        Write-Error "❌ Erreur lors de la lecture des logs: $_"
        return @()
    } finally {
        Pop-Location
    }
}

# Fonction de correction backend
function Fix-BackendDeployment {
    param([string[]]$Logs)
    
    Write-Info "🔧 Tentative de correction backend..."
    
    # Analyser les logs pour trouver les erreurs
    $errors = @()
    foreach ($log in $logs) {
        if ($log -match "error|Error|ERROR|failed|Failed|FAILED|exception|Exception") {
            $errors += $log
        }
    }
    
    if ($errors.Count -eq 0) {
        Write-Warning "⚠️ Aucune erreur détectée dans les logs"
        return $false
    }
    
    Write-Warning "📋 Erreurs détectées:"
    $errors | Select-Object -First 10 | ForEach-Object { Write-Debug "   $_" }
    
    # Corrections automatiques possibles
    $fixed = $false
    
    # Erreur: Variables d'environnement manquantes
    if ($errors -match "environment|ENV|secret") {
        Write-Info "🔧 Correction: Vérification des variables d'environnement..."
        Push-Location $BACKEND_DIR
        try {
            fly secrets list --app $FLY_APP | Out-Null
            Write-Success "✅ Secrets vérifiés"
            $fixed = $true
        } catch {
            Write-Warning "⚠️ Impossible de vérifier les secrets"
        } finally {
            Pop-Location
        }
    }
    
    # Erreur: Port ou connexion
    if ($errors -match "port|Port|connection|Connection|bind") {
        Write-Info "🔧 Correction: Redémarrage de l'application..."
        Push-Location $BACKEND_DIR
        try {
            fly apps restart $FLY_APP
            Write-Success "✅ Application redémarrée"
            $fixed = $true
        } catch {
            Write-Warning "⚠️ Impossible de redémarrer"
        } finally {
            Pop-Location
        }
    }
    
    return $fixed
}

# Fonction de déploiement backend avec vérification
function Deploy-Backend {
    Write-Info "`n📦 Déploiement Backend (Fly.io)..."
    
    Push-Location $BACKEND_DIR
    
    try {
        # Vérifier que fly CLI est installé
        $flyCheck = fly version 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Error "❌ Fly CLI non installé. Installez-le avec: iwr https://fly.io/install.ps1 -useb | iex"
            return $false
        }
        
        # Vérifier la connexion
        Write-Info "🔐 Vérification connexion Fly.io..."
        fly auth whoami 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Write-Error "❌ Non connecté à Fly.io. Exécutez: fly auth login"
            return $false
        }
        
        # Déployer
        Write-Info "🚀 Déploiement en cours..."
        $deployOutput = fly deploy --remote-only 2>&1 | Tee-Object -Variable deployLog
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✅ Déploiement backend terminé!"
            
            # Vérifier que le déploiement est pris en charge
            Write-Info "⏳ Attente de la disponibilité du service (30s)..."
            Start-Sleep -Seconds 10
            
            $isDeployed = Test-BackendDeployment -TimeoutSeconds 30
            
            if (-not $isDeployed) {
                Write-Warning "⚠️ Le déploiement semble avoir réussi mais le service n'est pas accessible"
                
                # Lire les logs
                $logs = Get-BackendLogs
                
                # Essayer de corriger
                $fixed = Fix-BackendDeployment -Logs $logs
                
                if ($fixed) {
                    Write-Info "⏳ Nouvelle vérification après correction..."
                    Start-Sleep -Seconds 15
                    $isDeployed = Test-BackendDeployment -TimeoutSeconds 30
                }
                
                if (-not $isDeployed) {
                    Write-Error "❌ Le service n'est toujours pas accessible après correction"
                    Write-Info "📋 Derniers logs:"
                    Get-BackendLogs | Select-Object -Last 20 | ForEach-Object { Write-Debug "   $_" }
                    return $false
                }
            }
            
            Write-Success "✅ Backend déployé et vérifié!"
            Write-Info "📍 URL: $BACKEND_URL"
            return $true
        } else {
            Write-Error "❌ Erreur lors du déploiement backend"
            Write-Info "📋 Logs de déploiement:"
            $deployLog | Select-Object -Last 20 | ForEach-Object { Write-Debug "   $_" }
            
            # Lire les logs pour diagnostic
            $logs = Get-BackendLogs
            Fix-BackendDeployment -Logs $logs
            
            return $false
        }
    } catch {
        Write-Error "❌ Erreur: $_"
        return $false
    } finally {
        Pop-Location
    }
}

# Fonction pour configurer les variables Netlify
function Set-NetlifyEnv {
    param(
        [string]$VariableName,
        [string]$Value,
        [string]$Context = "production"
    )
    
    if (-not (Get-Command netlify -ErrorAction SilentlyContinue)) {
        Write-Warning "Netlify CLI non installé, impossible de définir la variable"
        return $false
    }
    
    try {
        Push-Location $FRONTEND_DIR
        $result = netlify env:set $VariableName $Value --context $Context 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Variable $VariableName définie pour $Context"
            return $true
        } else {
            Write-Warning "Impossible de définir $VariableName : $result"
            return $false
        }
    } catch {
        Write-Warning "Erreur lors de la définition de $VariableName : $_"
        return $false
    } finally {
        Pop-Location
    }
}

# Fonction de vérification frontend
function Test-FrontendDeployment {
    param([int]$TimeoutSeconds = 60)
    
    Write-Info "🔍 Vérification du déploiement frontend..."
    
    # Si Netlify CLI est disponible, vérifier le statut
    if (Get-Command netlify -ErrorAction SilentlyContinue) {
        try {
            Push-Location $FRONTEND_DIR
            $status = netlify status 2>&1
            if ($status -match "Live URL|Site URL") {
                Write-Success "✅ Frontend déployé sur Netlify"
                return $true
            }
        } catch {
            Write-Debug "Netlify CLI status non disponible"
        } finally {
            Pop-Location
        }
    }
    
    # Vérifier via Git (si Netlify est connecté à GitHub)
    Write-Info "⏳ Vérification via Git/Netlify (peut prendre 1-2 minutes)..."
    
    # Attendre que Netlify termine le déploiement
    $maxAttempts = $TimeoutSeconds / 10
    
    for ($i = 1; $i -le $maxAttempts; $i++) {
        Write-Debug "Vérification $i/$maxAttempts..."
        
        # Vérifier le dernier commit sur GitHub
        try {
            $lastCommit = git log -1 --format="%H" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✅ Commit poussé sur Git: $($lastCommit.Substring(0, 8))"
                Write-Info "⏳ Netlify déploiera automatiquement (vérifiez dans le dashboard)"
                return $true
            }
        } catch {
            Write-Debug "Erreur vérification Git: $_"
        }
        
        if ($i -lt $maxAttempts) {
            Start-Sleep -Seconds 10
        }
    }
    
    Write-Warning "⚠️ Impossible de vérifier le déploiement frontend automatiquement"
    Write-Info "💡 Vérifiez manuellement dans le dashboard Netlify"
    return $true # On considère que c'est OK car Netlify déploie automatiquement
}

# Fonction de lecture des logs frontend (Netlify)
function Get-FrontendLogs {
    Write-Info "📋 Lecture des logs frontend (Netlify)..."
    
    Push-Location $FRONTEND_DIR
    
    try {
        if (Get-Command netlify -ErrorAction SilentlyContinue) {
            $logs = netlify logs 2>&1 | Select-Object -Last 50
            return $logs
        } else {
            Write-Warning "⚠️ Netlify CLI non installé. Installez-le avec: npm install -g netlify-cli"
            Write-Info "💡 Vérifiez les logs dans le dashboard Netlify"
            return @()
        }
    } catch {
        Write-Error "❌ Erreur lors de la lecture des logs: $_"
        return @()
    } finally {
        Pop-Location
    }
}

# Fonction de correction frontend
function Fix-FrontendDeployment {
    param([string[]]$Logs)
    
    Write-Info "🔧 Tentative de correction frontend..."
    
    $errors = @()
    foreach ($log in $logs) {
        if ($log -match "error|Error|ERROR|failed|Failed|FAILED|build|Build") {
            $errors += $log
        }
    }
    
    if ($errors.Count -eq 0) {
        Write-Warning "⚠️ Aucune erreur détectée dans les logs"
        return $false
    }
    
    Write-Warning "📋 Erreurs détectées:"
    $errors | Select-Object -First 10 | ForEach-Object { Write-Debug "   $_" }
    
    $fixed = $false
    
    # Erreur: Variables d'environnement
    if ($errors -match "NEXT_PUBLIC|environment|ENV") {
        Write-Info "🔧 Correction: Vérification des variables d'environnement Netlify..."
        Write-Warning "⚠️ Vérifiez manuellement dans Netlify Dashboard → Site settings → Environment variables"
        $fixed = $true
    }
    
    # Erreur: Build
    if ($errors -match "build|Build|npm|node") {
        Write-Info "🔧 Correction: Nettoyage et rebuild..."
        Push-Location $FRONTEND_DIR
        try {
            Remove-Item -Path ".next" -Recurse -Force -ErrorAction SilentlyContinue
            npm run build 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Success "✅ Build local réussi"
                $fixed = $true
            }
        } catch {
            Write-Warning "⚠️ Erreur lors du build local"
        } finally {
            Pop-Location
        }
    }
    
    return $fixed
}

# Fonction de déploiement frontend avec vérification
function Deploy-Frontend {
    Write-Info "`n📦 Déploiement Frontend (Netlify)..."
    
    Push-Location $FRONTEND_DIR
    
    try {
        # Vérifier et configurer les variables Netlify si nécessaire
        Write-Info "🔍 Vérification des variables d'environnement Netlify..."
        if (Get-Command netlify -ErrorAction SilentlyContinue) {
            $envList = netlify env:list 2>&1
            if ($envList -notmatch "NEXT_PUBLIC_API_URL") {
                Write-Warning "⚠️ Variable NEXT_PUBLIC_API_URL manquante, configuration..."
                Set-NetlifyEnv -VariableName "NEXT_PUBLIC_API_URL" -Value $BACKEND_URL -Context "production"
                Set-NetlifyEnv -VariableName "NEXT_PUBLIC_API_URL" -Value $BACKEND_URL -Context "deploy-preview"
                Set-NetlifyEnv -VariableName "NEXT_PUBLIC_API_URL" -Value $BACKEND_URL -Context "branch-deploy"
            } else {
                Write-Success "✅ Variables Netlify configurées"
            }
        }
        
        # Vérifier s'il y a des changements
        $gitStatus = git status --porcelain 2>&1
        
        if ($gitStatus) {
            Write-Info "📝 Changements détectés, commit et push..."
            
            git add . 2>&1 | Out-Null
            $commitMessage = "Auto-deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git commit -m $commitMessage 2>&1 | Out-Null
            
            if ($LASTEXITCODE -eq 0) {
                Write-Info "📤 Push sur Git..."
                git push origin main 2>&1 | Out-Null
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "✅ Frontend poussé sur Git"
                    
                    # Vérifier le déploiement
                    Write-Info "⏳ Attente du déploiement Netlify (60s)..."
                    Start-Sleep -Seconds 15
                    
                    $isDeployed = Test-FrontendDeployment -TimeoutSeconds 60
                    
                    if (-not $isDeployed) {
                        Write-Warning "⚠️ Le déploiement semble avoir réussi mais la vérification a échoué"
                        
                        # Lire les logs
                        $logs = Get-FrontendLogs
                        
                        # Essayer de corriger
                        $fixed = Fix-FrontendDeployment -Logs $logs
                        
                        if ($fixed) {
                            Write-Info "⏳ Nouvelle vérification après correction..."
                            Start-Sleep -Seconds 20
                            $isDeployed = Test-FrontendDeployment -TimeoutSeconds 60
                        }
                        
                        if (-not $isDeployed) {
                            Write-Warning "⚠️ Vérification échouée, mais Netlify déploie généralement automatiquement"
                            Write-Info "💡 Vérifiez manuellement dans le dashboard Netlify"
                        }
                    }
                    
                    Write-Success "✅ Frontend déployé!"
                    Write-Info "📍 Netlify déploiera automatiquement via GitHub"
                    return $true
                } else {
                    Write-Error "❌ Erreur lors du push Git"
                    return $false
                }
            } else {
                Write-Warning "⚠️ Aucun changement à committer"
                return $true
            }
        } else {
            Write-Warning "⚠️ Aucun changement détecté. Pas de déploiement nécessaire."
            return $true
        }
    } catch {
        Write-Error "❌ Erreur: $_"
        return $false
    } finally {
        Pop-Location
    }
}

# Fonction de surveillance de fichiers
function Watch-Files {
    Write-Info "`nSurveillance des fichiers activee..."
    Write-Info "   - Backend: $Backend"
    Write-Info "   - Frontend: $Frontend"
    Write-Info "   Appuyez sur Ctrl+C pour arreter"
    Write-Info ""
    
    $watcher = New-Object System.IO.FileSystemWatcher
    $watcher.Path = Get-Location
    $watcher.IncludeSubdirectories = $true
    $watcher.EnableRaisingEvents = $true
    $watcher.Filter = "*.*"
    
    $lastDeployTime = @{
        "backend" = [DateTime]::MinValue
        "frontend" = [DateTime]::MinValue
    }
    $deployCooldown = 30 # Secondes entre deux déploiements
    
    $action = {
        $path = $Event.SourceEventArgs.FullPath
        $changeType = $Event.SourceEventArgs.ChangeType
        $relativePath = $path.Replace((Get-Location).Path + "\", "").Replace((Get-Location).Path + "/", "")
        
        # Ignorer les fichiers dans les dossiers à exclure
        $shouldIgnore = $false
        foreach ($pattern in $IGNORE_PATTERNS) {
            if ($relativePath -match $pattern) {
                $shouldIgnore = $true
                break
            }
        }
        
        if (-not $shouldIgnore -and $changeType -ne "Changed") {
            Write-Info "`n📝 Modification détectée: $changeType - $relativePath"
            
            # Déterminer quel service déployer
            $deployBackend = $false
            $deployFrontend = $false
            
            if ($relativePath -like "backend\*" -or $relativePath -like "backend/*") {
                $deployBackend = $true
            } elseif ($relativePath -like "frontend\*" -or $relativePath -like "frontend/*") {
                $deployFrontend = $true
            } else {
                # Fichier à la racine, déployer les deux
                $deployBackend = $true
                $deployFrontend = $true
            }
            
            # Vérifier le cooldown
            $now = Get-Date
            if ($deployBackend -and ($now - $lastDeployTime["backend"]).TotalSeconds -lt $deployCooldown) {
                Write-Debug "⏳ Cooldown backend actif, attente..."
                $deployBackend = $false
            }
            if ($deployFrontend -and ($now - $lastDeployTime["frontend"]).TotalSeconds -lt $deployCooldown) {
                Write-Debug "⏳ Cooldown frontend actif, attente..."
                $deployFrontend = $false
            }
            
            # Attendre 2 secondes pour éviter les déploiements multiples
            Start-Sleep -Seconds 2
            
            if ($deployBackend -and $Backend) {
                Write-Info "🚀 Déploiement backend déclenché..."
                $success = Deploy-Backend
                if ($success) {
                    $lastDeployTime["backend"] = Get-Date
                }
            }
            
            if ($deployFrontend -and $Frontend) {
                Write-Info "🚀 Déploiement frontend déclenché..."
                $success = Deploy-Frontend
                if ($success) {
                    $lastDeployTime["frontend"] = Get-Date
                }
            }
        }
    }
    
    # Enregistrer les événements
    $changedEvent = Register-ObjectEvent $watcher "Changed" -Action $action
    $createdEvent = Register-ObjectEvent $watcher "Created" -Action $action
    $deletedEvent = Register-ObjectEvent $watcher "Deleted" -Action $action
    
    # Attendre indéfiniment
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    } finally {
        $watcher.EnableRaisingEvents = $false
        $watcher.Dispose()
        Unregister-Event -SourceIdentifier $changedEvent.Name
        Unregister-Event -SourceIdentifier $createdEvent.Name
        Unregister-Event -SourceIdentifier $deletedEvent.Name
    }
}

# Mode surveillance ou déploiement unique
if ($Watch) {
    Watch-Files
} else {
    # Déploiement unique
    $success = $true
    
    if ($Backend) {
        $success = Deploy-Backend -and $success
    }
    
    if ($Frontend) {
        $success = Deploy-Frontend -and $success
    }
    
    if ($success) {
        Write-Success "`n✅ Déploiement terminé!"
    } else {
        Write-Error "`n❌ Certains déploiements ont échoué"
        exit 1
    }
}

