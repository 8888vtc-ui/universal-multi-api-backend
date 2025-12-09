"""Test Medical APIs"""
import asyncio
from services.external_apis.medical_extended import disease_sh, open_disease, rxnorm

async def test_medical_apis():
    print("=" * 50)
    print("TESTING MEDICAL APIs")
    print("=" * 50)
    
    # Test 1: Disease.sh COVID
    print("\n1. Testing Disease.sh (COVID-19)...")
    try:
        covid = await disease_sh.get_covid_global()
        print(f"   Cases: {covid.get('cases'):,}")
        print(f"   Deaths: {covid.get('deaths'):,}")
        print(f"   Recovered: {covid.get('recovered'):,}")
        print("   [OK] Disease.sh working!")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 2: Local Disease Database
    print("\n2. Testing Open Disease (Local DB)...")
    try:
        diabetes = await open_disease.get_disease_info("diabetes")
        print(f"   Found: {diabetes.get('found')}")
        print(f"   Name: {diabetes.get('name')}")
        print(f"   Symptoms: {', '.join(diabetes.get('symptoms', [])[:3])}...")
        print("   [OK] Open Disease working!")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 3: RxNorm Drug Search
    print("\n3. Testing RxNorm (Drug Info)...")
    try:
        aspirin = await rxnorm.search_drug("aspirin")
        print(f"   Drugs found: {aspirin.get('count')}")
        if aspirin.get('drugs'):
            print(f"   First result: {aspirin['drugs'][0].get('name')}")
        print("   [OK] RxNorm working!")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print("\n" + "=" * 50)
    print("ALL MEDICAL APIs TESTED!")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(test_medical_apis())
