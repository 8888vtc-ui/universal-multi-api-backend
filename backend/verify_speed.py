
import asyncio
import httpx
import time
import json

BASE_URL = "https://universal-api-hub.fly.dev"
# BASE_URL = "http://localhost:8000"

async def test_endpoint(name, payload, expected_time=5.0):
    print(f"\n--- Testing {name} ---")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    start_time = time.time()
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{BASE_URL}/api/expert/expert_general_fr/chat",
                json=payload
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                print(f"Status: {response.status_code}")
                print(f"Time: {duration:.2f}s")
                print(f"Response (snippet): {data['response'][:100]}...")
                print(f"Source: {data.get('source', 'Unknown')}")
                print(f"Processing Info: {data.get('processing_time_ms', 'N/A')}ms")
                
                if duration < expected_time:
                    print(f"✅ PASS (Faster than {expected_time}s)")
                else:
                    print(f"⚠️ SLOW (Slower than {expected_time}s)")
            else:
                print(f"❌ FAIL: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

async def main():
    # TEST 1: Simple Query (Should use 8B Turbo)
    await test_endpoint(
        "Simple Query (Expecting Turbo 8B)",
        {
            "message": "Bonjour, comment vas-tu ?",
            "session_id": "test_speed_1",
            "language": "fr"
        },
        expected_time=2.0
    )
    
    # TEST 2: Complex Query (Cold Cache)
    await test_endpoint(
        "Complex Query (Cold Cache - Expecting 70B + API)",
        {
            "message": "Quelles sont les dernières nouvelles sur Elon Musk aujourd'hui ?",
            "session_id": "test_speed_2",
            "language": "fr"
        },
        expected_time=8.0
    )
    
    # TEST 3: Complex Query (Warm Cache)
    await test_endpoint(
        "Complex Query (Warm Cache - Expecting Cache Hit for Data)",
        {
            "message": "Quelles sont les dernières nouvelles sur Elon Musk aujourd'hui ?",
            "session_id": "test_speed_3",
            "language": "fr"
        },
        expected_time=5.0
    )

if __name__ == "__main__":
    asyncio.run(main())
