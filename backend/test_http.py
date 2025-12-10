import httpx
import asyncio

async def test():
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://api.open-meteo.com/v1/forecast?latitude=48&longitude=2&current_weather=true")
            print(f"Status: {response.status_code}")
            print(f"Data: {response.text[:200]}")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

asyncio.run(test())
