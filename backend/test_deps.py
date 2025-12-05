"""
Quick test script for backend dependencies
"""
import sys

print("Testing backend dependencies...")
print(f"Python version: {sys.version}")

# Test imports
packages = {
    'fastapi': 'FastAPI',
    'groq': 'Groq',
    'redis': 'Redis',
    'pydantic': 'Pydantic',
    'uvicorn': 'Uvicorn',
}

missing = []
for package, name in packages.items():
    try:
        __import__(package)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} - NOT INSTALLED")
        missing.append(package)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)
else:
    print("\n✅ All core packages installed!")
    sys.exit(0)
