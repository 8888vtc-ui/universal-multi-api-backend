"""
Tourism Query Router - Routage intelligent pour l'expert Tourisme
Détecte l'intention et appelle les APIs pertinentes
"""
import re
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from datetime import datetime
import logging
import os

logger = logging.getLogger(__name__)


class TourismIntent(Enum):
    """Types d'intentions pour le tourisme"""
    FLIGHTS = "flights"
    WEATHER = "weather"
    DESTINATION = "destination"
    ADVICE = "advice"
    EXCHANGE = "exchange"
    GENERAL = "general"


class TourismQueryRouter:
    """Routeur intelligent pour les requêtes touristiques"""
    
    def __init__(self):
        self.geocoding_router = None
        self.weather_router = None
        self._init_routers()
    
    def _init_routers(self):
        """Initialiser les routers"""
        try:
            from services.external_apis.geocoding import GeocodingRouter
            from services.external_apis.weather.router import WeatherRouter
            self.geocoding_router = GeocodingRouter()
            self.weather_router = WeatherRouter()
            logger.info("✅ TourismQueryRouter initialized with geocoding and weather")
        except Exception as e:
            logger.warning(f"Failed to init routers: {e}")
    
    def detect_intent(self, query: str) -> Tuple[TourismIntent, Dict[str, Any]]:
        """Détecte l'intention et extrait les entités"""
        query_lower = query.lower()
        entities = {}
        
        # 1. FLIGHTS
        if re.search(r'\b(vol|flight|vols|flights|billet|ticket|avion|plane|partir|départ|arrivée)\b', query_lower):
            airports = self._extract_airports(query)
            if airports.get('from') and airports.get('to'):
                entities.update(airports)
                return TourismIntent.FLIGHTS, entities
        
        # 2. WEATHER
        if re.search(r'\b(météo|weather|temps|climat|température)\b', query_lower):
            destination = self._extract_destination(query)
            if destination:
                entities['destination'] = destination
                return TourismIntent.WEATHER, entities
        
        # 3. EXCHANGE
        if re.search(r'\b(change|exchange|taux|rate|monnaie|currency|euro|dollar|convertir)\b', query_lower):
            return TourismIntent.EXCHANGE, entities
        
        # 4. DESTINATION
        if re.search(r'\b(visiter|visit|voir|see|faire|do|attractions|à voir|to see)\b', query_lower):
            destination = self._extract_destination(query)
            if destination:
                entities['destination'] = destination
                return TourismIntent.DESTINATION, entities
        
        # 5. ADVICE
        if re.search(r'\b(conseil|advice|meilleur|best|période|period|quand|when|budget|coût)\b', query_lower):
            destination = self._extract_destination(query)
            if destination:
                entities['destination'] = destination
                return TourismIntent.ADVICE, entities
        
        # 6. GENERAL
        destination = self._extract_destination(query)
        if destination:
            entities['destination'] = destination
        return TourismIntent.GENERAL, entities
    
    def _extract_destination(self, query: str) -> Optional[str]:
        """Extrait le nom de la destination"""
        patterns = [
            r'\b(?:à|in|to|for|de|du|en)\s+([A-Z][a-zéèêëàâäùûüôöîïç]+(?:\s+[A-Z][a-zéèêëàâäùûüôöîïç]+)*)',
            r'\b([A-Z][a-zéèêëàâäùûüôöîïç]+(?:\s+[A-Z][a-zéèêëàâäùûüôöîïç]+)*)\b',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, query)
            if matches:
                return matches[-1].strip()
        return None
    
    def _extract_airports(self, query: str) -> Dict[str, Optional[str]]:
        """Extrait les aéroports/villes de départ et d'arrivée"""
        pattern = r'([A-Za-zéèêëàâäùûüôöîïç]+(?:\s+[A-Za-zéèêëàâäùûüôöîïç]+)?)\s*[-–—]\s*([A-Za-zéèêëàâäùûüôöîïç]+(?:\s+[A-Za-zéèêëàâäùûüôöîïç]+)?)'
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return {'from': match.group(1).strip(), 'to': match.group(2).strip()}
        
        pattern2 = r'(?:from|depuis|de)\s+([A-Za-zéèêëàâäùûüôöîïç]+(?:\s+[A-Za-zéèêëàâäùûüôöîïç]+)?)\s+(?:to|vers|à)\s+([A-Za-zéèêëàâäùûüôöîïç]+(?:\s+[A-Za-zéèêëàâäùûüôöîïç]+)?)'
        match2 = re.search(pattern2, query, re.IGNORECASE)
        if match2:
            return {'from': match2.group(1).strip(), 'to': match2.group(2).strip()}
        
        return {'from': None, 'to': None}
    
    async def get_comprehensive_tourism_info(self, query: str) -> Dict[str, Any]:
        """Récupère les informations touristiques complètes"""
        intent, entities = self.detect_intent(query)
        logger.info(f"[TOURISM] Intent: {intent.value}, entities: {entities}")
        
        result = {
            "query": query,
            "intent": intent.value,
            "entities": entities,
            "timestamp": datetime.now().isoformat(),
            "data": {}
        }
        
        tasks = []
        
        # Routage selon l'intention
        if intent == TourismIntent.FLIGHTS:
            if entities.get('from') and entities.get('to'):
                tasks.append(("flights", self._get_flights_info(entities['from'], entities['to'])))
                tasks.append(("geocoding_from", self._get_geocoding(entities['from'])))
                tasks.append(("geocoding_to", self._get_geocoding(entities['to'])))
        
        elif intent == TourismIntent.WEATHER:
            destination = entities.get('destination') or query
            tasks.append(("geocoding", self._get_geocoding(destination)))
        
        elif intent == TourismIntent.DESTINATION:
            destination = entities.get('destination') or query
            tasks.append(("geocoding", self._get_geocoding(destination)))
            tasks.append(("countries", self._get_country_info(destination)))
            tasks.append(("wikipedia", self._get_wikipedia_info(destination)))
        
        elif intent == TourismIntent.ADVICE:
            destination = entities.get('destination') or query
            tasks.append(("geocoding", self._get_geocoding(destination)))
            tasks.append(("countries", self._get_country_info(destination)))
            tasks.append(("exchange", self._get_exchange_rates()))
        
        else:  # GENERAL
            destination = entities.get('destination') or query
            tasks.append(("geocoding", self._get_geocoding(destination)))
            tasks.append(("countries", self._get_country_info(destination)))
            tasks.append(("wikipedia", self._get_wikipedia_info(destination)))
        
        # Exécuter en parallèle
        if tasks:
            task_results = await asyncio.gather(
                *[task[1] for task in tasks],
                return_exceptions=True
            )
            
            for (task_name, _), task_result in zip(tasks, task_results):
                if isinstance(task_result, Exception):
                    logger.warning(f"[TOURISM] Task {task_name} failed: {task_result}")
                    result["data"][task_name] = {"error": str(task_result)}
                else:
                    result["data"][task_name] = task_result
                    logger.info(f"[TOURISM] ✅ Task {task_name} success")
            
            # Si géocodage réussi, récupérer météo
            geo_data = result["data"].get("geocoding", {})
            if geo_data and not geo_data.get("error"):
                if geo_data.get("results"):
                    location = geo_data["results"][0]
                    lat = location.get("lat")
                    lon = location.get("lon")
                    
                    if lat and lon and self.weather_router:
                        try:
                            weather_data = await self.weather_router.get_current_weather(float(lat), float(lon))
                            result["data"]["weather"] = weather_data
                            logger.info(f"[TOURISM] ✅ Weather retrieved for {lat}, {lon}")
                        except Exception as e:
                            logger.warning(f"[TOURISM] Weather failed: {e}")
        
        return result
    
    async def _get_flights_info(self, from_city: str, to_city: str) -> Dict[str, Any]:
        """Récupère les informations de vols"""
        try:
            from services.http_client import http_client
            query_str = f"{from_city}-{to_city}"
            response = await http_client.get(
                "http://localhost:8000/api/flights/search",
                params={"query": query_str, "limit": 10}
            )
            if response.status_code == 200:
                return response.json()
            return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_geocoding(self, location: str) -> Dict[str, Any]:
        """Récupère le géocodage"""
        if not self.geocoding_router:
            return {"error": "Geocoding router not available"}
        try:
            return await self.geocoding_router.search(location)
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_country_info(self, destination: str) -> Dict[str, Any]:
        """Récupère les infos pays"""
        try:
            from services.http_client import http_client
            response = await http_client.get(
                "http://localhost:8000/api/countries/search",
                params={"q": destination}
            )
            if response.status_code == 200:
                return response.json()
            return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_wikipedia_info(self, destination: str) -> Dict[str, Any]:
        """Récupère les infos Wikipedia"""
        try:
            from services.external_apis.wikipedia.provider import WikipediaProvider
            wiki = WikipediaProvider()
            results = await wiki.search(destination, limit=2)
            return {"results": results}
        except Exception as e:
            return {"error": str(e)}
    
    async def _get_exchange_rates(self) -> Dict[str, Any]:
        """Récupère les taux de change"""
        try:
            from services.http_client import http_client
            response = await http_client.get("https://open.er-api.com/v6/latest/EUR")
            if response.status_code == 200:
                data = response.json()
                rates = data.get("rates", {})
                return {
                    "base": "EUR",
                    "rates": {k: rates.get(k) for k in ["USD", "GBP", "JPY", "CNY", "CHF", "ILS"] if k in rates}
                }
            return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}


def format_tourism_context(data: Dict[str, Any]) -> str:
    """Formate les données touristiques pour le contexte IA"""
    parts = []
    
    parts.append("═══════════════════════════════════════════════════════")
    parts.append(f"🌍 RECHERCHE TOURISTIQUE - {data.get('intent', 'general').upper()}")
    parts.append("═══════════════════════════════════════════════════════")
    parts.append("")
    
    entities = data.get("entities", {})
    if entities:
        parts.append("📍 ENTITÉS EXTRAITES:")
        for key, value in entities.items():
            if value:
                parts.append(f"  • {key}: {value}")
        parts.append("")
    
    api_data = data.get("data", {})
    
    # Géocodage
    if "geocoding" in api_data:
        geo = api_data["geocoding"]
        if not geo.get("error") and geo.get("results"):
            location = geo["results"][0]
            parts.append("🗺️ LOCALISATION:")
            parts.append(f"  • Lieu: {location.get('name', 'N/A')}")
            parts.append(f"  • Pays: {location.get('country', 'N/A')}")
            parts.append(f"  • Coordonnées: {location.get('lat', 'N/A')}, {location.get('lon', 'N/A')}")
            parts.append("")
    
    # Météo
    if "weather" in api_data:
        weather = api_data["weather"]
        if not weather.get("error"):
            parts.append("🌡️ MÉTÉO ACTUELLE:")
            parts.append(f"  • Température: {weather.get('temperature', 'N/A')}°C")
            parts.append(f"  • Vent: {weather.get('windspeed', 'N/A')} km/h")
            if weather.get('condition'):
                parts.append(f"  • Conditions: {weather.get('condition')}")
            parts.append("")
    
    # Vols
    if "flights" in api_data:
        flights = api_data["flights"]
        if not flights.get("error") and flights.get("flights"):
            parts.append("✈️ VOLS DISPONIBLES:")
            for flight in flights["flights"][:5]:
                dep = flight.get('departure', {})
                arr = flight.get('arrival', {})
                parts.append(f"  • {flight.get('airline', 'N/A')} {flight.get('flight_number', '')}: {dep.get('airport', 'N/A')} → {arr.get('airport', 'N/A')}")
            parts.append("")
    
    # Pays
    if "countries" in api_data:
        countries = api_data["countries"]
        if not countries.get("error") and countries.get("countries"):
            country = countries["countries"][0]
            parts.append("🌍 INFORMATIONS PAYS:")
            parts.append(f"  • Capitale: {country.get('capital', 'N/A')}")
            if country.get('population'):
                parts.append(f"  • Population: {country.get('population'):,}")
            if country.get('languages'):
                langs = country.get('languages', [])
                if isinstance(langs, list):
                    parts.append(f"  • Langues: {', '.join(langs)}")
                elif isinstance(langs, dict):
                    parts.append(f"  • Langues: {', '.join(langs.values())}")
            if country.get('currencies'):
                parts.append(f"  • Monnaie: {', '.join(country.get('currencies', []))}")
            parts.append("")
    
    # Wikipedia
    if "wikipedia" in api_data:
        wiki = api_data["wikipedia"]
        if not wiki.get("error") and wiki.get("results"):
            parts.append("📚 INFORMATIONS (Wikipedia):")
            for article in wiki["results"][:2]:
                snippet = article.get('snippet', '')[:200]
                parts.append(f"  • {article.get('title', 'N/A')}: {snippet}...")
            parts.append("")
    
    # Taux de change
    if "exchange" in api_data:
        exchange = api_data["exchange"]
        if not exchange.get("error") and exchange.get("rates"):
            parts.append("💱 TAUX DE CHANGE (base EUR):")
            rates = exchange["rates"]
            for currency, rate in rates.items():
                parts.append(f"  • 1 EUR = {rate} {currency}")
            parts.append("")
    
    # Sources
    sources = [k for k, v in api_data.items() if not v.get("error")]
    if sources:
        parts.append(f"[SOURCES]: {', '.join(sources)}")
    
    return "\n".join(parts)


# Singleton
tourism_router = TourismQueryRouter()
