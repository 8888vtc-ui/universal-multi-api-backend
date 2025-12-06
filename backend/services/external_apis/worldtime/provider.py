"""World Time Provider - Timezone and time data"""
import httpx
from typing import Dict, Any, List
from datetime import datetime, timezone
import pytz

class WorldTimeProvider:
    """Provider for World Time API (free, unlimited)"""
    
    # Common timezones as fallback
    COMMON_TIMEZONES = [
        "Africa/Cairo", "Africa/Johannesburg", "America/Chicago", "America/Denver",
        "America/Los_Angeles", "America/New_York", "America/Sao_Paulo", "America/Toronto",
        "Asia/Dubai", "Asia/Hong_Kong", "Asia/Jerusalem", "Asia/Kolkata", "Asia/Shanghai",
        "Asia/Singapore", "Asia/Tokyo", "Australia/Melbourne", "Australia/Sydney",
        "Europe/Berlin", "Europe/London", "Europe/Moscow", "Europe/Paris", "Pacific/Auckland"
    ]
    
    def __init__(self):
        self.base_url = "http://worldtimeapi.org/api"
        self.available = True
        print("✅ World Time API provider initialized (free, unlimited)")
    
    def _get_local_time(self, tz_name: str) -> Dict[str, Any]:
        """Get time using local pytz"""
        try:
            tz = pytz.timezone(tz_name)
            now = datetime.now(tz)
            return {
                "timezone": tz_name,
                "datetime": now.isoformat(),
                "utc_offset": str(now.strftime('%z')),
                "day_of_week": now.weekday(),
                "day_of_year": now.timetuple().tm_yday,
                "week_number": now.isocalendar()[1],
                "source": "local"
            }
        except:
            return None
    
    async def get_timezone(self, timezone_name: str) -> Dict[str, Any]:
        """Get time for a specific timezone"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/timezone/{timezone_name}")
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback to local calculation
            result = self._get_local_time(timezone_name)
            if result:
                return result
            
            raise Exception(f"Timezone {timezone_name} not found")
    
    async def get_ip_time(self, ip: str = None) -> Dict[str, Any]:
        """Get time based on IP address"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                if ip:
                    response = await client.get(f"{self.base_url}/ip/{ip}")
                else:
                    response = await client.get(f"{self.base_url}/ip")
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback to UTC
            return self._get_local_time("UTC")
    
    async def get_timezones(self) -> List[str]:
        """Get list of all available timezones"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(f"{self.base_url}/timezone")
                if response.status_code == 200:
                    return response.json()
            except:
                pass
            
            # Fallback to pytz timezones
            return list(pytz.common_timezones)

