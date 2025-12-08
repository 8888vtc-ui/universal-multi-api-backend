# Script PowerShell pour vérifier la progression du test
$reportFile = "backend/stress_test_report.json"

Write-Host "`n🔍 Vérification de la progression du test...`n"

if (Test-Path $reportFile) {
    try {
        $report = Get-Content $reportFile -Raw | ConvertFrom-Json
        $summary = $report.summary
        
        Write-Host "📊 STATUT ACTUEL:" -ForegroundColor Cyan
        Write-Host "   Questions testées: $($summary.total_questions)" -ForegroundColor White
        Write-Host "   ✅ Réussies: $($summary.successful)" -ForegroundColor Green
        Write-Host "   ❌ Échouées: $($summary.failed)" -ForegroundColor Red
        Write-Host "   📈 Taux de succès: $($summary.success_rate)" -ForegroundColor Yellow
        
        if ($summary.average_response_time_ms) {
            Write-Host "   ⏱️  Temps moyen: $([math]::Round($summary.average_response_time_ms, 0))ms" -ForegroundColor White
        }
        
        if ($summary.questions_per_second) {
            Write-Host "   🚀 Vitesse: $([math]::Round($summary.questions_per_second, 2)) questions/s" -ForegroundColor White
        }
        
        # Erreurs critiques
        $criticalErrors = $report.critical_errors
        if ($criticalErrors -and $criticalErrors.Count -gt 0) {
            Write-Host "`n🚨 ERREURS CRITIQUES DÉTECTÉES: $($criticalErrors.Count)" -ForegroundColor Red
            foreach ($error in $criticalErrors[0..4]) {
                Write-Host "   - Question $($error.question_num): $($error.error_type)" -ForegroundColor Red
            }
        }
        
        # Erreurs par type
        $errorsByType = $report.errors_by_type
        if ($errorsByType -and ($errorsByType.PSObject.Properties.Count -gt 0)) {
            Write-Host "`n⚠️  ERREURS PAR TYPE:" -ForegroundColor Yellow
            $errorsByType.PSObject.Properties | Sort-Object Value -Descending | ForEach-Object {
                Write-Host "   - $($_.Name): $($_.Value)" -ForegroundColor Yellow
            }
        }
        
        # Vérifier si le test est terminé
        if ($report.stop_requested) {
            Write-Host "`nTEST ARRETE - Erreur critique detectee" -ForegroundColor Red
        } elseif ($summary.total_questions -ge 5000) {
            Write-Host "`nTEST TERMINE - 5000 questions completees" -ForegroundColor Green
        } else {
            $remaining = 5000 - $summary.total_questions
            $estimatedTime = if ($summary.questions_per_second -gt 0) {
                [math]::Round($remaining / $summary.questions_per_second / 60, 1)
            } else { "?" }
            Write-Host "`n⏳ TEST EN COURS - $remaining questions restantes (~$estimatedTime min)" -ForegroundColor Cyan
        }
        
    } catch {
        Write-Host "⚠️  Erreur lors de la lecture du rapport: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "⏳ Le test démarre... Le rapport sera créé prochainement." -ForegroundColor Yellow
    Write-Host "   Vérifiez à nouveau dans quelques secondes." -ForegroundColor Gray
}

Write-Host ""



Write-Host "`n🔍 Vérification de la progression du test...`n"

if (Test-Path $reportFile) {
    try {
        $report = Get-Content $reportFile -Raw | ConvertFrom-Json
        $summary = $report.summary
        
        Write-Host "📊 STATUT ACTUEL:" -ForegroundColor Cyan
        Write-Host "   Questions testées: $($summary.total_questions)" -ForegroundColor White
        Write-Host "   ✅ Réussies: $($summary.successful)" -ForegroundColor Green
        Write-Host "   ❌ Échouées: $($summary.failed)" -ForegroundColor Red
        Write-Host "   📈 Taux de succès: $($summary.success_rate)" -ForegroundColor Yellow
        
        if ($summary.average_response_time_ms) {
            Write-Host "   ⏱️  Temps moyen: $([math]::Round($summary.average_response_time_ms, 0))ms" -ForegroundColor White
        }
        
        if ($summary.questions_per_second) {
            Write-Host "   🚀 Vitesse: $([math]::Round($summary.questions_per_second, 2)) questions/s" -ForegroundColor White
        }
        
        # Erreurs critiques
        $criticalErrors = $report.critical_errors
        if ($criticalErrors -and $criticalErrors.Count -gt 0) {
            Write-Host "`n🚨 ERREURS CRITIQUES DÉTECTÉES: $($criticalErrors.Count)" -ForegroundColor Red
            foreach ($error in $criticalErrors[0..4]) {
                Write-Host "   - Question $($error.question_num): $($error.error_type)" -ForegroundColor Red
            }
        }
        
        # Erreurs par type
        $errorsByType = $report.errors_by_type
        if ($errorsByType -and ($errorsByType.PSObject.Properties.Count -gt 0)) {
            Write-Host "`n⚠️  ERREURS PAR TYPE:" -ForegroundColor Yellow
            $errorsByType.PSObject.Properties | Sort-Object Value -Descending | ForEach-Object {
                Write-Host "   - $($_.Name): $($_.Value)" -ForegroundColor Yellow
            }
        }
        
        # Vérifier si le test est terminé
        if ($report.stop_requested) {
            Write-Host "`nTEST ARRETE - Erreur critique detectee" -ForegroundColor Red
        } elseif ($summary.total_questions -ge 5000) {
            Write-Host "`nTEST TERMINE - 5000 questions completees" -ForegroundColor Green
        } else {
            $remaining = 5000 - $summary.total_questions
            $estimatedTime = if ($summary.questions_per_second -gt 0) {
                [math]::Round($remaining / $summary.questions_per_second / 60, 1)
            } else { "?" }
            Write-Host "`n⏳ TEST EN COURS - $remaining questions restantes (~$estimatedTime min)" -ForegroundColor Cyan
        }
        
    } catch {
        Write-Host "⚠️  Erreur lors de la lecture du rapport: $_" -ForegroundColor Yellow
    }
} else {
    Write-Host "⏳ Le test démarre... Le rapport sera créé prochainement." -ForegroundColor Yellow
    Write-Host "   Vérifiez à nouveau dans quelques secondes." -ForegroundColor Gray
}

Write-Host ""

