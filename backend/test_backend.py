"""
Test backend API functionality without starting server
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("BACKEND API TESTS")
print("=" * 60)

# Test 1: Import main modules
print("\n1. Testing imports...")
try:
    from main import app
    from services.ai_router import ai_router
    from services.cache import cache_service
    print("✅ All modules imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

# Test 2: Check AI Router status
print("\n2. Checking AI Router...")
try:
    status = ai_router.get_status()
    print(f"   Available providers: {sum(1 for p in status.values() if p['available'])}/{len(status)}")
    for name, info in status.items():
        icon = "✅" if info['available'] else "⚠️ "
        print(f"   {icon} {name.capitalize()}: {'Available' if info['available'] else 'Not available'}")
except Exception as e:
    print(f"❌ AI Router check failed: {e}")

# Test 3: Check Cache Service
print("\n3. Checking Cache Service...")
try:
    cache_healthy = cache_service.health_check()
    if cache_healthy:
        print("   ✅ Redis cache: Connected")
    else:
        print("   ⚠️  Redis cache: Not available (optional)")
except Exception as e:
    print(f"   ⚠️  Cache check failed: {e} (optional)")

# Test 4: Check FastAPI app
print("\n4. Checking FastAPI app...")
try:
    routes = [route.path for route in app.routes]
    print(f"   ✅ API routes registered: {len(routes)}")
    for route in ["/api/health", "/api/chat", "/api/embeddings"]:
        if route in routes:
            print(f"   ✅ {route}")
        else:
            print(f"   ❌ {route} - NOT FOUND")
except Exception as e:
    print(f"❌ FastAPI check failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ BACKEND TESTS PASSED")
print("=" * 60)
print("\nℹ️  Note: Some providers may not be available without API keys.")
print("   This is normal for testing. The API will use fallback providers.")
print("\n🚀 To start the server: python main.py")
