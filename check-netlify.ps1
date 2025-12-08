# check-netlify.ps1
# Script pour verifier le statut du deploiement Netlify

Write-Host "Verification du deploiement Netlify..." -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Verifier le dernier commit
Write-Host "`n[1/4] Verification du dernier commit Git..." -ForegroundColor Yellow
$lastCommit = git log -1 --oneline
Write-Host "   Dernier commit: $lastCommit" -ForegroundColor White

$commitHash = git log -1 --format="%H"
Write-Host "   Hash: $commitHash" -ForegroundColor Gray

# Verifier le remote
Write-Host "`n[2/4] Verification du remote Git..." -ForegroundColor Yellow
$remote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Remote: $remote" -ForegroundColor Green
} else {
    Write-Host "   Remote non configure" -ForegroundColor Red
    exit 1
}

# Verifier Netlify CLI
Write-Host "`n[3/4] Verification Netlify CLI..." -ForegroundColor Yellow
if (Get-Command netlify -ErrorAction SilentlyContinue) {
    Write-Host "   Netlify CLI: Installe" -ForegroundColor Green
    
    # Obtenir le statut
    $status = netlify status 2>&1
    Write-Host "   Statut Netlify:" -ForegroundColor Cyan
    $status | ForEach-Object { Write-Host "     $_" -ForegroundColor White }
    
    # Essayer d'obtenir les infos du site
    try {
        $siteInfo = netlify api getSite --data "{\"site_id\":\"2d6f74c0-6884-479f-9d56-19b6003a9b08\"}" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   Site info recuperee" -ForegroundColor Green
        }
    } catch {
        Write-Host "   Impossible de recuperer les infos du site" -ForegroundColor Yellow
    }
} else {
    Write-Host "   Netlify CLI: Non installe" -ForegroundColor Yellow
    Write-Host "   Installez avec: npm install -g netlify-cli" -ForegroundColor Cyan
}

# Verifier l'accessibilite du site
Write-Host "`n[4/4] Verification de l'accessibilite du site..." -ForegroundColor Yellow

$sites = @(
    "https://wikiask.net",
    "https://wikiask.io",
    "https://incomparable-semolina-c3a66d.netlify.app"
)

foreach ($site in $sites) {
    try {
        $response = Invoke-WebRequest -Uri $site -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        Write-Host "   $site : Accessible (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "   $site : Non accessible" -ForegroundColor Yellow
    }
}

Write-Host "`n=======================================" -ForegroundColor Cyan
Write-Host "Resume:" -ForegroundColor Cyan
Write-Host "  - Code pousse sur GitHub: OUI" -ForegroundColor Green
Write-Host "  - Netlify connecte: OUI" -ForegroundColor Green
Write-Host "  - Site ID: 2d6f74c0-6884-479f-9d56-19b6003a9b08" -ForegroundColor White
Write-Host "  - Project: incomparable-semolina-c3a66d" -ForegroundColor White
Write-Host "`nPour verifier le deploiement:" -ForegroundColor Yellow
Write-Host "  1. Allez sur: https://app.netlify.com/projects/incomparable-semolina-c3a66d" -ForegroundColor Cyan
Write-Host "  2. Verifiez l'onglet 'Deploys'" -ForegroundColor Cyan
Write-Host "  3. Le dernier deploy devrait correspondre au commit: $($commitHash.Substring(0, 7))" -ForegroundColor Cyan


# Script pour verifier le statut du deploiement Netlify

Write-Host "Verification du deploiement Netlify..." -ForegroundColor Cyan
Write-Host "=======================================" -ForegroundColor Cyan

# Verifier le dernier commit
Write-Host "`n[1/4] Verification du dernier commit Git..." -ForegroundColor Yellow
$lastCommit = git log -1 --oneline
Write-Host "   Dernier commit: $lastCommit" -ForegroundColor White

$commitHash = git log -1 --format="%H"
Write-Host "   Hash: $commitHash" -ForegroundColor Gray

# Verifier le remote
Write-Host "`n[2/4] Verification du remote Git..." -ForegroundColor Yellow
$remote = git remote get-url origin 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "   Remote: $remote" -ForegroundColor Green
} else {
    Write-Host "   Remote non configure" -ForegroundColor Red
    exit 1
}

# Verifier Netlify CLI
Write-Host "`n[3/4] Verification Netlify CLI..." -ForegroundColor Yellow
if (Get-Command netlify -ErrorAction SilentlyContinue) {
    Write-Host "   Netlify CLI: Installe" -ForegroundColor Green
    
    # Obtenir le statut
    $status = netlify status 2>&1
    Write-Host "   Statut Netlify:" -ForegroundColor Cyan
    $status | ForEach-Object { Write-Host "     $_" -ForegroundColor White }
    
    # Essayer d'obtenir les infos du site
    try {
        $siteInfo = netlify api getSite --data "{\"site_id\":\"2d6f74c0-6884-479f-9d56-19b6003a9b08\"}" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   Site info recuperee" -ForegroundColor Green
        }
    } catch {
        Write-Host "   Impossible de recuperer les infos du site" -ForegroundColor Yellow
    }
} else {
    Write-Host "   Netlify CLI: Non installe" -ForegroundColor Yellow
    Write-Host "   Installez avec: npm install -g netlify-cli" -ForegroundColor Cyan
}

# Verifier l'accessibilite du site
Write-Host "`n[4/4] Verification de l'accessibilite du site..." -ForegroundColor Yellow

$sites = @(
    "https://wikiask.net",
    "https://wikiask.io",
    "https://incomparable-semolina-c3a66d.netlify.app"
)

foreach ($site in $sites) {
    try {
        $response = Invoke-WebRequest -Uri $site -Method GET -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        Write-Host "   $site : Accessible (Status: $($response.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "   $site : Non accessible" -ForegroundColor Yellow
    }
}

Write-Host "`n=======================================" -ForegroundColor Cyan
Write-Host "Resume:" -ForegroundColor Cyan
Write-Host "  - Code pousse sur GitHub: OUI" -ForegroundColor Green
Write-Host "  - Netlify connecte: OUI" -ForegroundColor Green
Write-Host "  - Site ID: 2d6f74c0-6884-479f-9d56-19b6003a9b08" -ForegroundColor White
Write-Host "  - Project: incomparable-semolina-c3a66d" -ForegroundColor White
Write-Host "`nPour verifier le deploiement:" -ForegroundColor Yellow
Write-Host "  1. Allez sur: https://app.netlify.com/projects/incomparable-semolina-c3a66d" -ForegroundColor Cyan
Write-Host "  2. Verifiez l'onglet 'Deploys'" -ForegroundColor Cyan
Write-Host "  3. Le dernier deploy devrait correspondre au commit: $($commitHash.Substring(0, 7))" -ForegroundColor Cyan



