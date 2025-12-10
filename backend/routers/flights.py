"""
Flights API Router - AviationStack
Recherche de vols et informations aéroports
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
import os
import logging
import re

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/flights", tags=["flights"])

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
AVIATIONSTACK_BASE_URL = "https://api.aviationstack.com/v1"


@router.get("/search")
async def search_flights(
    query: str = Query(..., description="Flight search query (e.g., 'Paris-Tokyo', 'CDG-NRT')"),
    limit: int = Query(10, ge=1, le=100, description="Number of results")
):
    """
    Search flights using AviationStack API
    
    Query format:
    - "Paris-Tokyo" → Search flights between cities
    - "CDG-NRT" → Search flights between airports
    - "Paris" → Search flights from/to Paris
    """
    from services.http_client import http_client
    
    if not AVIATIONSTACK_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AviationStack API key not configured. Set AVIATIONSTACK_API_KEY environment variable."
        )
    
    try:
        # Parser la requête pour extraire départ/arrivée
        from_city, to_city = _parse_flight_query(query)
        
        # Appeler AviationStack API
        params = {
            "access_key": AVIATIONSTACK_API_KEY,
            "limit": limit
        }
        
        # Si on a départ et arrivée, chercher des vols
        if from_city and to_city:
            # Chercher les aéroports pour ces villes
            airports_from = await _get_airports_by_city(from_city)
            airports_to = await _get_airports_by_city(to_city)
            
            if airports_from and airports_to:
                # Utiliser le premier aéroport de chaque ville
                params["dep_iata"] = airports_from[0].get("iata_code")
                params["arr_iata"] = airports_to[0].get("iata_code")
        
        # Appel API AviationStack
        response = await http_client.get(
            f"{AVIATIONSTACK_BASE_URL}/flights",
            params=params
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AviationStack API error: {response.text}"
            )
        
        data = response.json()
        
        # Formater la réponse
        flights = data.get("data", [])
        formatted_flights = []
        
        for flight in flights[:limit]:
            formatted_flights.append({
                "flight_number": flight.get("flight", {}).get("iata", "N/A"),
                "airline": flight.get("airline", {}).get("name", "N/A"),
                "departure": {
                    "airport": flight.get("departure", {}).get("airport", "N/A"),
                    "iata": flight.get("departure", {}).get("iata", "N/A"),
                    "scheduled": flight.get("departure", {}).get("scheduled", "N/A"),
                    "timezone": flight.get("departure", {}).get("timezone", "N/A")
                },
                "arrival": {
                    "airport": flight.get("arrival", {}).get("airport", "N/A"),
                    "iata": flight.get("arrival", {}).get("iata", "N/A"),
                    "scheduled": flight.get("arrival", {}).get("scheduled", "N/A"),
                    "timezone": flight.get("arrival", {}).get("timezone", "N/A")
                },
                "aircraft": flight.get("aircraft", {}).get("iata", "N/A"),
                "status": flight.get("flight_status", "unknown")
            })
        
        return {
            "success": True,
            "query": query,
            "from": from_city,
            "to": to_city,
            "count": len(formatted_flights),
            "flights": formatted_flights
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Flights search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Flights search failed: {str(e)}"
        )


@router.get("/airports")
async def get_airports(
    city: Optional[str] = Query(None, description="City name"),
    iata: Optional[str] = Query(None, description="Airport IATA code")
):
    """Get airport information"""
    from services.http_client import http_client
    
    if not AVIATIONSTACK_API_KEY:
        raise HTTPException(status_code=503, detail="AviationStack API key not configured")
    
    try:
        params = {"access_key": AVIATIONSTACK_API_KEY}
        
        if iata:
            params["iata_code"] = iata
        elif city:
            params["city_name"] = city
        
        response = await http_client.get(
            f"{AVIATIONSTACK_BASE_URL}/airports",
            params=params
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="AviationStack API error")
        
        data = response.json()
        airports = data.get("data", [])
        
        return {
            "success": True,
            "count": len(airports),
            "airports": airports[:20]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Airports search failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def flights_status():
    """Check flights API status"""
    return {
        "success": True,
        "api_key_configured": bool(AVIATIONSTACK_API_KEY),
        "provider": "AviationStack"
    }


def _parse_flight_query(query: str) -> tuple:
    """Parse flight query to extract from/to cities"""
    # Pattern: "Paris-Tokyo", "Paris to Tokyo", "CDG-NRT"
    pattern1 = r'([A-Za-z]+(?:\s+[A-Za-z]+)?)\s*[-–—]\s*([A-Za-z]+(?:\s+[A-Za-z]+)?)'
    match1 = re.search(pattern1, query, re.IGNORECASE)
    if match1:
        return match1.group(1).strip(), match1.group(2).strip()
    
    # Pattern: "from X to Y"
    pattern2 = r'(?:from|depuis|de)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)\s+(?:to|vers|à)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)'
    match2 = re.search(pattern2, query, re.IGNORECASE)
    if match2:
        return match2.group(1).strip(), match2.group(2).strip()
    
    return None, None


async def _get_airports_by_city(city: str) -> list:
    """Get airports for a city"""
    from services.http_client import http_client
    
    try:
        params = {
            "access_key": AVIATIONSTACK_API_KEY,
            "city_name": city
        }
        
        response = await http_client.get(
            f"{AVIATIONSTACK_BASE_URL}/airports",
            params=params
        )
        
        if response.status_code == 200:
            data = response.json()
            return data.get("data", [])
        return []
    except:
        return []
