@echo off
echo ========================================
echo   Universal API Hub - Demarrage
echo ========================================
echo.

:: Demarrer le backend
echo [1/2] Demarrage du Backend...
start "Backend" cmd /k "cd backend && python main.py"

:: Attendre que le backend demarre
timeout /t 10 /nobreak > nul

:: Demarrer le frontend
echo [2/2] Demarrage du Frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Tout est demarre!
echo ========================================
echo.
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   Docs:     http://localhost:8000/docs
echo.
echo Appuyez sur une touche pour fermer...
pause > nul






