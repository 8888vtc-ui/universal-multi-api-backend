import httpx
import asyncio

async def test():
    url = "https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        print(f"Status: {r.status_code}")
        print(f"Data: {r.text[:300]}")

asyncio.run(test())
