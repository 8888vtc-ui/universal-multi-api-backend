# Script PowerShell pour vérifier la progression du test d'hallucinations
$reportFile = "backend\hallucination_test_report.json"

if (Test-Path $reportFile) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "📊 RAPPORT DE DÉTECTION D'HALLUCINATIONS" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    $report = Get-Content $reportFile -Raw | ConvertFrom-Json
    
    $summary = $report.summary
    
    Write-Host "✅ Questions réussies: " -NoNewline
    Write-Host $summary.successful -ForegroundColor Green
    
    Write-Host "❌ Questions échouées: " -NoNewline
    Write-Host $summary.failed -ForegroundColor Red
    
    Write-Host "🚨 Hallucinations détectées: " -NoNewline
    Write-Host $summary.hallucinations_detected -ForegroundColor Yellow
    
    Write-Host "📈 Taux d'hallucinations: " -NoNewline
    Write-Host ("{0:N2}%" -f $summary.hallucination_rate) -ForegroundColor Yellow
    
    Write-Host "⏱️  Temps total: " -NoNewline
    Write-Host ("{0:N2}s" -f $summary.total_time_seconds) -ForegroundColor Cyan
    
    Write-Host "⚡ Vitesse: " -NoNewline
    Write-Host ("{0:N2} questions/s" -f $summary.questions_per_second) -ForegroundColor Cyan
    
    Write-Host "`n💡 Pour analyser les résultats: python backend\scripts\analyze_hallucinations.py" -ForegroundColor Green
} else {
    Write-Host "⏳ Le test est en cours de démarrage..." -ForegroundColor Yellow
    Write-Host "   Le rapport sera disponible une fois le test terminé." -ForegroundColor Yellow
}


$reportFile = "backend\hallucination_test_report.json"

if (Test-Path $reportFile) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "📊 RAPPORT DE DÉTECTION D'HALLUCINATIONS" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    $report = Get-Content $reportFile -Raw | ConvertFrom-Json
    
    $summary = $report.summary
    
    Write-Host "✅ Questions réussies: " -NoNewline
    Write-Host $summary.successful -ForegroundColor Green
    
    Write-Host "❌ Questions échouées: " -NoNewline
    Write-Host $summary.failed -ForegroundColor Red
    
    Write-Host "🚨 Hallucinations détectées: " -NoNewline
    Write-Host $summary.hallucinations_detected -ForegroundColor Yellow
    
    Write-Host "📈 Taux d'hallucinations: " -NoNewline
    Write-Host ("{0:N2}%" -f $summary.hallucination_rate) -ForegroundColor Yellow
    
    Write-Host "⏱️  Temps total: " -NoNewline
    Write-Host ("{0:N2}s" -f $summary.total_time_seconds) -ForegroundColor Cyan
    
    Write-Host "⚡ Vitesse: " -NoNewline
    Write-Host ("{0:N2} questions/s" -f $summary.questions_per_second) -ForegroundColor Cyan
    
    Write-Host "`n💡 Pour analyser les résultats: python backend\scripts\analyze_hallucinations.py" -ForegroundColor Green
} else {
    Write-Host "⏳ Le test est en cours de démarrage..." -ForegroundColor Yellow
    Write-Host "   Le rapport sera disponible une fois le test terminé." -ForegroundColor Yellow
}



