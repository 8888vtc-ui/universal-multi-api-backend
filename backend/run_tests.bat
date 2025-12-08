@echo off
echo ========================================
echo TESTS - MOTEUR DE RECHERCHE UNIVERSEL
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Tests unitaires...
pytest tests/test_search.py -v
if %errorlevel% neq 0 (
    echo ERREUR: Tests unitaires echoues
    pause
    exit /b 1
)

echo.
echo [2/3] Tests d'integration...
pytest tests/test_search_integration.py -v -m integration
if %errorlevel% neq 0 (
    echo ATTENTION: Tests d'integration echoues (peut etre normal si APIs non configurees)
)

echo.
echo [3/3] Resume...
pytest --tb=short -q

echo.
echo ========================================
echo TESTS TERMINES
echo ========================================
pause


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes
