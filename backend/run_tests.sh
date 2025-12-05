#!/bin/bash

echo "========================================"
echo "TESTS - MOTEUR DE RECHERCHE UNIVERSEL"
echo "========================================"
echo ""

cd "$(dirname "$0")"

echo "[1/3] Tests unitaires..."
pytest tests/test_search.py -v
if [ $? -ne 0 ]; then
    echo "ERREUR: Tests unitaires echoues"
    exit 1
fi

echo ""
echo "[2/3] Tests d'integration..."
pytest tests/test_search_integration.py -v -m integration
if [ $? -ne 0 ]; then
    echo "ATTENTION: Tests d'integration echoues (peut etre normal si APIs non configurees)"
fi

echo ""
echo "[3/3] Resume..."
pytest --tb=short -q

echo ""
echo "========================================"
echo "TESTS TERMINES"
echo "========================================"


