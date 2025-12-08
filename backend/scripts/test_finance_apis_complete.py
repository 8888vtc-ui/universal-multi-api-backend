"""
Test Complet des APIs Finance
Teste toutes les APIs finance disponibles et génère un rapport détaillé
"""
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.external_apis.finance import coingecko, alphavantage, yahoo_finance
from services.external_apis.coincap.provider import CoinCapProvider
from services.external_apis.exchange.provider import ExchangeRateProvider

# Importer les nouveaux providers
try:
    from services.external_apis.finnhub.provider import finnhub
except ImportError:
    finnhub = None

try:
    from services.external_apis.twelve_data.provider import twelve_data
except ImportError:
    twelve_data = None

coincap = CoinCapProvider()
exchange = ExchangeRateProvider()

# Test symbols
TEST_SYMBOLS = {
    "stocks": ["AAPL", "MSFT", "TSLA", "QQQ", "SPY"],
    "crypto": ["bitcoin", "ethereum", "btc", "eth"],
    "indices": ["^GSPC", "^DJI", "^IXIC"]
}

RESULTS = {
    "timestamp": datetime.now().isoformat(),
    "providers": {},
    "summary": {
        "total_tests": 0,
        "success": 0,
        "failed": 0,
        "success_rate": 0.0
    }
}


async def test_coingecko():
    """Test CoinGecko API"""
    provider_name = "CoinGecko"
    results = {"available": coingecko.available, "tests": []}
    
    if not coingecko.available:
        results["error"] = "Provider not available"
        return results
    
    # Test 1: Bitcoin price
    try:
        start = time.time()
        data = await coingecko.get_crypto_price("bitcoin", "usd")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_crypto_price(bitcoin)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "data_keys": list(data.keys())[:5]
            })
        else:
            results["tests"].append({
                "test": "get_crypto_price(bitcoin)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_crypto_price(bitcoin)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    # Test 2: Trending
    try:
        start = time.time()
        data = await coingecko.get_trending()
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_trending()",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "has_data": True
            })
        else:
            results["tests"].append({
                "test": "get_trending()",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_trending()",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_yahoo_finance():
    """Test Yahoo Finance API"""
    provider_name = "Yahoo Finance"
    results = {"available": yahoo_finance.available, "tests": []}
    
    if not yahoo_finance.available:
        results["error"] = "Provider not available"
        return results
    
    # Test 1: Stock info (AAPL)
    try:
        start = time.time()
        data = await yahoo_finance.get_stock_info("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_info(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price"),
                "symbol": data.get("symbol")
            })
        else:
            results["tests"].append({
                "test": "get_stock_info(AAPL)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_info(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    # Test 2: Market summary
    try:
        start = time.time()
        data = await yahoo_finance.get_market_summary()
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and len(data) > 0:
            results["tests"].append({
                "test": "get_market_summary()",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "indices_count": len(data),
                "indices": list(data.keys())
            })
        else:
            results["tests"].append({
                "test": "get_market_summary()",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_market_summary()",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    # Test 3: QQQ (NASDAQ ETF)
    try:
        start = time.time()
        data = await yahoo_finance.get_stock_info("QQQ")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_info(QQQ)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price")
            })
        else:
            results["tests"].append({
                "test": "get_stock_info(QQQ)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_info(QQQ)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_alphavantage():
    """Test Alpha Vantage API"""
    provider_name = "Alpha Vantage"
    results = {"available": alphavantage.available, "tests": []}
    
    if not alphavantage.available:
        results["error"] = "API key not configured"
        return results
    
    # Test stock quote
    try:
        start = time.time()
        data = await alphavantage.get_stock_quote("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "has_data": True
            })
        else:
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_quote(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_coincap():
    """Test CoinCap API"""
    provider_name = "CoinCap"
    results = {"available": coincap.available, "tests": []}
    
    if not coincap.available:
        results["error"] = "Provider not available"
        return results
    
    # Test assets search
    try:
        start = time.time()
        data = await coincap.get_assets(limit=10, search="bitcoin")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("data"):
            results["tests"].append({
                "test": "get_assets(bitcoin)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "assets_count": len(data.get("data", []))
            })
        else:
            results["tests"].append({
                "test": "get_assets(bitcoin)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_assets(bitcoin)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_finnhub():
    """Test Finnhub API"""
    if not finnhub:
        return {"available": False, "error": "Provider not imported"}
    
    results = {"available": finnhub.available, "tests": []}
    
    if not finnhub.available:
        results["error"] = "Provider not available"
        return results
    
    # Test stock quote
    try:
        start = time.time()
        data = await finnhub.get_stock_quote("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price")
            })
        else:
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_quote(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_twelve_data():
    """Test Twelve Data API"""
    if not twelve_data:
        return {"available": False, "error": "Provider not imported"}
    
    results = {"available": twelve_data.available, "tests": []}
    
    if not twelve_data.available:
        results["error"] = "API key not configured"
        return results
    
    # Test stock quote
    try:
        start = time.time()
        data = await twelve_data.get_stock_quote("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price")
            })
        else:
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_quote(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_exchange():
    """Test Exchange Rate API"""
    results = {"available": True, "tests": []}
    
    try:
        start = time.time()
        data = await exchange.get_rates("USD")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_rates(USD)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "rates_count": len(data.get("rates", {}))
            })
        else:
            results["tests"].append({
                "test": "get_rates(USD)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_rates(USD)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def run_all_tests():
    """Run all finance API tests"""
    print("[INFO] Test Complet des APIs Finance")
    print("=" * 60)
    
    # Run all tests in parallel where possible
    test_functions = [
        ("CoinGecko", test_coingecko),
        ("Yahoo Finance", test_yahoo_finance),
        ("Alpha Vantage", test_alphavantage),
        ("CoinCap", test_coincap),
        ("Finnhub", test_finnhub),
        ("Twelve Data", test_twelve_data),
        ("Exchange Rate", test_exchange),
    ]
    
    for name, test_func in test_functions:
        print(f"\n📊 Testing {name}...")
        try:
            result = await test_func()
            RESULTS["providers"][name] = result
            
            # Count successes
            if "tests" in result:
                for test in result["tests"]:
                    RESULTS["summary"]["total_tests"] += 1
                    if test["status"] == "success":
                        RESULTS["summary"]["success"] += 1
                    else:
                        RESULTS["summary"]["failed"] += 1
        except Exception as e:
            print(f"[ERR] Error testing {name}: {e}")
            RESULTS["providers"][name] = {
                "available": False,
                "error": str(e)[:200]
            }
    
    # Calculate success rate
    if RESULTS["summary"]["total_tests"] > 0:
        RESULTS["summary"]["success_rate"] = (
            RESULTS["summary"]["success"] / RESULTS["summary"]["total_tests"] * 100
        )
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Total tests: {RESULTS['summary']['total_tests']}")
    print(f"[OK] Succès: {RESULTS['summary']['success']}")
    print(f"[ERR] Échecs: {RESULTS['summary']['failed']}")
    print(f"📈 Taux de succès: {RESULTS['summary']['success_rate']:.1f}%")
    
    # Print per-provider summary
    print("\n" + "=" * 60)
    print("📋 DÉTAIL PAR PROVIDER")
    print("=" * 60)
    for name, result in RESULTS["providers"].items():
        available = "[OK]" if result.get("available") else "[ERR]"
        print(f"\n{available} {name}")
        if "error" in result:
            print(f"   Erreur: {result['error']}")
        if "tests" in result:
            for test in result["tests"]:
                status = "[OK]" if test["status"] == "success" else "[ERR]"
                print(f"   {status} {test['test']}")
                if test["status"] == "success" and "time_ms" in test:
                    print(f"      Temps: {test['time_ms']}ms")
                elif test["status"] == "failed":
                    print(f"      Erreur: {test.get('error', 'Unknown')}")
    
    # Save report
    report_file = "finance_apis_test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport sauvegardé: {report_file}")
    
    return RESULTS


if __name__ == "__main__":
    asyncio.run(run_all_tests())


Test Complet des APIs Finance
Teste toutes les APIs finance disponibles et génère un rapport détaillé
"""
import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Any
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.external_apis.finance import coingecko, alphavantage, yahoo_finance
from services.external_apis.coincap.provider import CoinCapProvider
from services.external_apis.exchange.provider import ExchangeRateProvider

# Importer les nouveaux providers
try:
    from services.external_apis.finnhub.provider import finnhub
except ImportError:
    finnhub = None

try:
    from services.external_apis.twelve_data.provider import twelve_data
except ImportError:
    twelve_data = None

coincap = CoinCapProvider()
exchange = ExchangeRateProvider()

# Test symbols
TEST_SYMBOLS = {
    "stocks": ["AAPL", "MSFT", "TSLA", "QQQ", "SPY"],
    "crypto": ["bitcoin", "ethereum", "btc", "eth"],
    "indices": ["^GSPC", "^DJI", "^IXIC"]
}

RESULTS = {
    "timestamp": datetime.now().isoformat(),
    "providers": {},
    "summary": {
        "total_tests": 0,
        "success": 0,
        "failed": 0,
        "success_rate": 0.0
    }
}


async def test_coingecko():
    """Test CoinGecko API"""
    provider_name = "CoinGecko"
    results = {"available": coingecko.available, "tests": []}
    
    if not coingecko.available:
        results["error"] = "Provider not available"
        return results
    
    # Test 1: Bitcoin price
    try:
        start = time.time()
        data = await coingecko.get_crypto_price("bitcoin", "usd")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_crypto_price(bitcoin)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "data_keys": list(data.keys())[:5]
            })
        else:
            results["tests"].append({
                "test": "get_crypto_price(bitcoin)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_crypto_price(bitcoin)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    # Test 2: Trending
    try:
        start = time.time()
        data = await coingecko.get_trending()
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_trending()",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "has_data": True
            })
        else:
            results["tests"].append({
                "test": "get_trending()",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_trending()",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_yahoo_finance():
    """Test Yahoo Finance API"""
    provider_name = "Yahoo Finance"
    results = {"available": yahoo_finance.available, "tests": []}
    
    if not yahoo_finance.available:
        results["error"] = "Provider not available"
        return results
    
    # Test 1: Stock info (AAPL)
    try:
        start = time.time()
        data = await yahoo_finance.get_stock_info("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_info(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price"),
                "symbol": data.get("symbol")
            })
        else:
            results["tests"].append({
                "test": "get_stock_info(AAPL)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_info(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    # Test 2: Market summary
    try:
        start = time.time()
        data = await yahoo_finance.get_market_summary()
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and len(data) > 0:
            results["tests"].append({
                "test": "get_market_summary()",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "indices_count": len(data),
                "indices": list(data.keys())
            })
        else:
            results["tests"].append({
                "test": "get_market_summary()",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_market_summary()",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    # Test 3: QQQ (NASDAQ ETF)
    try:
        start = time.time()
        data = await yahoo_finance.get_stock_info("QQQ")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_info(QQQ)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price")
            })
        else:
            results["tests"].append({
                "test": "get_stock_info(QQQ)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_info(QQQ)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_alphavantage():
    """Test Alpha Vantage API"""
    provider_name = "Alpha Vantage"
    results = {"available": alphavantage.available, "tests": []}
    
    if not alphavantage.available:
        results["error"] = "API key not configured"
        return results
    
    # Test stock quote
    try:
        start = time.time()
        data = await alphavantage.get_stock_quote("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "has_data": True
            })
        else:
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_quote(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_coincap():
    """Test CoinCap API"""
    provider_name = "CoinCap"
    results = {"available": coincap.available, "tests": []}
    
    if not coincap.available:
        results["error"] = "Provider not available"
        return results
    
    # Test assets search
    try:
        start = time.time()
        data = await coincap.get_assets(limit=10, search="bitcoin")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("data"):
            results["tests"].append({
                "test": "get_assets(bitcoin)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "assets_count": len(data.get("data", []))
            })
        else:
            results["tests"].append({
                "test": "get_assets(bitcoin)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_assets(bitcoin)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_finnhub():
    """Test Finnhub API"""
    if not finnhub:
        return {"available": False, "error": "Provider not imported"}
    
    results = {"available": finnhub.available, "tests": []}
    
    if not finnhub.available:
        results["error"] = "Provider not available"
        return results
    
    # Test stock quote
    try:
        start = time.time()
        data = await finnhub.get_stock_quote("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price")
            })
        else:
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_quote(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_twelve_data():
    """Test Twelve Data API"""
    if not twelve_data:
        return {"available": False, "error": "Provider not imported"}
    
    results = {"available": twelve_data.available, "tests": []}
    
    if not twelve_data.available:
        results["error"] = "API key not configured"
        return results
    
    # Test stock quote
    try:
        start = time.time()
        data = await twelve_data.get_stock_quote("AAPL")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict) and data.get("price"):
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "price": data.get("price")
            })
        else:
            results["tests"].append({
                "test": "get_stock_quote(AAPL)",
                "status": "failed",
                "error": "No price data"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_stock_quote(AAPL)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def test_exchange():
    """Test Exchange Rate API"""
    results = {"available": True, "tests": []}
    
    try:
        start = time.time()
        data = await exchange.get_rates("USD")
        elapsed = (time.time() - start) * 1000
        
        if data and isinstance(data, dict):
            results["tests"].append({
                "test": "get_rates(USD)",
                "status": "success",
                "time_ms": round(elapsed, 2),
                "rates_count": len(data.get("rates", {}))
            })
        else:
            results["tests"].append({
                "test": "get_rates(USD)",
                "status": "failed",
                "error": "No data returned"
            })
    except Exception as e:
        results["tests"].append({
            "test": "get_rates(USD)",
            "status": "failed",
            "error": str(e)[:200]
        })
    
    return results


async def run_all_tests():
    """Run all finance API tests"""
    print("[INFO] Test Complet des APIs Finance")
    print("=" * 60)
    
    # Run all tests in parallel where possible
    test_functions = [
        ("CoinGecko", test_coingecko),
        ("Yahoo Finance", test_yahoo_finance),
        ("Alpha Vantage", test_alphavantage),
        ("CoinCap", test_coincap),
        ("Finnhub", test_finnhub),
        ("Twelve Data", test_twelve_data),
        ("Exchange Rate", test_exchange),
    ]
    
    for name, test_func in test_functions:
        print(f"\n📊 Testing {name}...")
        try:
            result = await test_func()
            RESULTS["providers"][name] = result
            
            # Count successes
            if "tests" in result:
                for test in result["tests"]:
                    RESULTS["summary"]["total_tests"] += 1
                    if test["status"] == "success":
                        RESULTS["summary"]["success"] += 1
                    else:
                        RESULTS["summary"]["failed"] += 1
        except Exception as e:
            print(f"[ERR] Error testing {name}: {e}")
            RESULTS["providers"][name] = {
                "available": False,
                "error": str(e)[:200]
            }
    
    # Calculate success rate
    if RESULTS["summary"]["total_tests"] > 0:
        RESULTS["summary"]["success_rate"] = (
            RESULTS["summary"]["success"] / RESULTS["summary"]["total_tests"] * 100
        )
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"Total tests: {RESULTS['summary']['total_tests']}")
    print(f"[OK] Succès: {RESULTS['summary']['success']}")
    print(f"[ERR] Échecs: {RESULTS['summary']['failed']}")
    print(f"📈 Taux de succès: {RESULTS['summary']['success_rate']:.1f}%")
    
    # Print per-provider summary
    print("\n" + "=" * 60)
    print("📋 DÉTAIL PAR PROVIDER")
    print("=" * 60)
    for name, result in RESULTS["providers"].items():
        available = "[OK]" if result.get("available") else "[ERR]"
        print(f"\n{available} {name}")
        if "error" in result:
            print(f"   Erreur: {result['error']}")
        if "tests" in result:
            for test in result["tests"]:
                status = "[OK]" if test["status"] == "success" else "[ERR]"
                print(f"   {status} {test['test']}")
                if test["status"] == "success" and "time_ms" in test:
                    print(f"      Temps: {test['time_ms']}ms")
                elif test["status"] == "failed":
                    print(f"      Erreur: {test.get('error', 'Unknown')}")
    
    # Save report
    report_file = "finance_apis_test_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(RESULTS, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Rapport sauvegardé: {report_file}")
    
    return RESULTS


if __name__ == "__main__":
    asyncio.run(run_all_tests())



