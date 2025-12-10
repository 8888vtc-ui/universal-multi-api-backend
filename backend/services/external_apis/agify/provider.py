"""Agify, Genderize, Nationalize Providers"""
import httpx
from typing import Dict, Any, List, Optional
from services.http_client import http_client

class NameAnalysisProvider:
    """Provider for Agify, Genderize, Nationalize APIs (free, 1,000/day each)"""
    
    def __init__(self):
        self.available = True
        print("[OK] Name Analysis APIs initialized (free, 1,000/day each)")
    
    async def predict_age(self, name: str, country_id: Optional[str] = None) -> Dict[str, Any]:
        """Predict age from name (Agify API)"""
        params = {"name": name}
        if country_id:
            params["country_id"] = country_id
        
        response = await http_client.get("https://api.agify.io", params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "name": data.get("name"),
            "predicted_age": data.get("age"),
            "count": data.get("count"),
            "country_id": country_id
        }
    
    async def predict_gender(self, name: str, country_id: Optional[str] = None) -> Dict[str, Any]:
        """Predict gender from name (Genderize API)"""
        params = {"name": name}
        if country_id:
            params["country_id"] = country_id
        
        response = await http_client.get("https://api.genderize.io", params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            "name": data.get("name"),
            "gender": data.get("gender"),
            "probability": data.get("probability"),
            "count": data.get("count"),
            "country_id": country_id
        }
    
    async def predict_nationality(self, name: str) -> Dict[str, Any]:
        """Predict nationality from name (Nationalize API)"""
        response = await http_client.get(
            "https://api.nationalize.io",
            params={"name": name}
        )
        response.raise_for_status()
        data = response.json()
        
        countries = []
        for c in data.get("country", [])[:5]:
            countries.append({
                "country_id": c.get("country_id"),
                "probability": round(c.get("probability", 0) * 100, 1)
            })
        
        return {
            "name": data.get("name"),
            "countries": countries,
            "count": data.get("count")
        }
    
    async def analyze_name(self, name: str, country_id: Optional[str] = None) -> Dict[str, Any]:
        """Full name analysis: age, gender, nationality"""
        import asyncio
        
        age_task = self.predict_age(name, country_id)
        gender_task = self.predict_gender(name, country_id)
        nationality_task = self.predict_nationality(name)
        
        age, gender, nationality = await asyncio.gather(
            age_task, gender_task, nationality_task,
            return_exceptions=True
        )
        
        result = {"name": name}
        
        if not isinstance(age, Exception):
            result["age"] = age.get("predicted_age")
        if not isinstance(gender, Exception):
            result["gender"] = gender.get("gender")
            result["gender_probability"] = gender.get("probability")
        if not isinstance(nationality, Exception):
            result["nationalities"] = nationality.get("countries", [])
        
        return result






