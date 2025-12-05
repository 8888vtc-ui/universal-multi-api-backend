"""
Aggregated API Endpoints
Combine multiple APIs to provide complete information in a single call
NO TIME WASTED - All APIs called in parallel, results combined intelligently
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from services.ai_router import ai_router
from services.external_apis.weather import WeatherRouter
from services.external_apis.geocoding import GeocodingRouter
from services.external_apis.news import NewsRouter
from services.external_apis.translation import TranslationRouter
from services.external_apis.nutrition import NutritionRouter
from services.external_apis import pubmed, openfda, coingecko, yahoo_finance
import asyncio

router = APIRouter(prefix="/api/aggregated", tags=["aggregated"])

# Initialize routers
weather_router = WeatherRouter()
geocoding_router = GeocodingRouter()
news_router = NewsRouter()
translation_router = TranslationRouter()
nutrition_router = NutritionRouter()


class TravelRecommendationRequest(BaseModel):
    """Request for travel recommendations"""
    destination: str
    language: str = "en"
    include_weather: bool = True
    include_restaurants: bool = True
    include_news: bool = True


class MarketAnalysisRequest(BaseModel):
    """Request for market analysis"""
    symbol: Optional[str] = None  # Stock or crypto symbol
    coin_id: Optional[str] = None  # Crypto coin ID
    include_news: bool = True
    include_ai_analysis: bool = True


class HealthRecommendationRequest(BaseModel):
    """Request for health recommendations"""
    query: str
    include_nutrition: bool = True
    include_medical: bool = True
    include_ai_advice: bool = True


@router.post("/travel/recommendations")
async def get_travel_recommendations(request: TravelRecommendationRequest):
    """
    Get complete travel recommendations combining multiple APIs
    
    Combines: Geocoding + Weather + IA + News + Translation
    Returns complete travel information in one call
    """
    try:
        results = {}
        errors = []
        
        # Run all API calls in parallel for speed
        tasks = []
        
        # 1. Geocoding
        if request.destination:
            tasks.append(("geocoding", geocoding_router.geocode(request.destination)))
        
        # 2. Weather (will use geocoding result if available)
        weather_task = None
        if request.include_weather:
            # First get geocoding, then weather
            pass  # Will handle after geocoding
        
        # 3. News about destination
        if request.include_news:
            tasks.append(("news", news_router.search(f"{request.destination} travel", language=request.language)))
        
        # Execute all in parallel
        task_results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        # Process results
        geocoding_data = None
        weather_data = None
        news_data = None
        
        for i, (task_name, task_result) in enumerate(zip([t[0] for t in tasks], task_results)):
            if isinstance(task_result, Exception):
                errors.append(f"{task_name}: {str(task_result)}")
            else:
                if task_name == "geocoding":
                    geocoding_data = task_result
                elif task_name == "news":
                    news_data = task_result
        
        # Get weather if geocoding succeeded
        if request.include_weather and geocoding_data:
            try:
                lat = geocoding_data.get('latitude')
                lon = geocoding_data.get('longitude')
                if lat and lon:
                    weather_data = await weather_router.get_current_weather(lat, lon)
            except Exception as e:
                errors.append(f"weather: {str(e)}")
        
        # 4. AI Analysis combining all data
        location_info = geocoding_data.get('formatted_address', request.destination) if geocoding_data else request.destination
        weather_info = f"{weather_data.get('temperature', 'N/A')}°C, {weather_data.get('description', 'N/A')}" if weather_data else "N/A"
        news_info = news_data.get('articles', [])[:3] if news_data else []
        
        ai_prompt = f"""
        Provide travel recommendations for {request.destination}.
        
        Location: {location_info}
        Weather: {weather_info}
        Recent News: {news_info}
        
        Provide:
        1. Best time to visit
        2. Must-see attractions
        3. Local tips
        4. Safety recommendations
        5. Cultural notes
        """
        
        ai_response = await ai_router.route(ai_prompt, language=request.language)
        
        return {
            "success": True,
            "destination": request.destination,
            "geocoding": geocoding_data,
            "weather": weather_data,
            "news": news_data,
            "ai_recommendations": ai_response.get("response"),
            "ai_source": ai_response.get("source"),
            "errors": errors if errors else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/market/analysis")
async def get_market_analysis(request: MarketAnalysisRequest):
    """
    Get complete market analysis combining Finance + News + IA
    
    Combines: Stock/Crypto prices + News + AI analysis
    Returns complete market intelligence in one call
    """
    try:
        results = {}
        errors = []
        
        tasks = []
        
        # 1. Get price data
        if request.symbol:
            # Import yahoo_finance function
            from services.external_apis import yahoo_finance
            tasks.append(("stock", yahoo_finance.get_stock_info(request.symbol)))
        elif request.coin_id:
            tasks.append(("crypto", coingecko.get_crypto_price(request.coin_id)))
        
        # 2. Get news
        if request.include_news:
            search_query = request.symbol or request.coin_id or "market"
            tasks.append(("news", news_router.search(search_query, language="en")))
        
        # Execute in parallel
        task_results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        price_data = None
        news_data = None
        
        for i, (task_name, task_result) in enumerate(zip([t[0] for t in tasks], task_results)):
            if isinstance(task_result, Exception):
                errors.append(f"{task_name}: {str(task_result)}")
            else:
                if task_name == "stock" or task_name == "crypto":
                    price_data = task_result
                elif task_name == "news":
                    news_data = task_result
        
        # 3. AI Analysis
        if request.include_ai_analysis:
            price_info = "N/A"
            if price_data:
                if isinstance(price_data, dict):
                    price_info = f"${price_data.get('price', price_data.get('currentPrice', 'N/A'))}"
                    change_info = price_data.get('price_change_24h', price_data.get('changePercent', 'N/A'))
                else:
                    price_info = str(price_data)
                    change_info = "N/A"
            else:
                change_info = "N/A"
            
            news_info = news_data.get('articles', [])[:5] if news_data else []
            
            ai_prompt = f"""
            Analyze the market for {request.symbol or request.coin_id}.
            
            Current Price: {price_info}
            Price Change: {change_info}%
            Recent News: {news_info}
            
            Provide:
            1. Market sentiment analysis
            2. Key factors affecting price
            3. Short-term outlook
            4. Risk assessment
            5. Investment recommendation
            """
            
            ai_response = await ai_router.route(ai_prompt)
            results["ai_analysis"] = ai_response.get("response")
            results["ai_source"] = ai_response.get("source")
        
        return {
            "success": True,
            "symbol": request.symbol or request.coin_id,
            "price_data": price_data,
            "news": news_data,
            **results,
            "errors": errors if errors else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/health/recommendations")
async def get_health_recommendations(request: HealthRecommendationRequest):
    """
    Get complete health recommendations combining Nutrition + Medical + IA
    
    Combines: Nutrition data + Medical research + AI advice
    Returns personalized health recommendations in one call
    """
    try:
        results = {}
        errors = []
        
        tasks = []
        
        # 1. Nutrition data
        if request.include_nutrition:
            tasks.append(("nutrition", nutrition_router.search_foods(request.query)))
        
        # 2. Medical research
        if request.include_medical:
            tasks.append(("medical", pubmed.search_articles(request.query, max_results=5)))
        
        # Execute in parallel
        task_results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        nutrition_data = None
        medical_data = None
        
        for i, (task_name, task_result) in enumerate(zip([t[0] for t in tasks], task_results)):
            if isinstance(task_result, Exception):
                errors.append(f"{task_name}: {str(task_result)}")
            else:
                if task_name == "nutrition":
                    nutrition_data = task_result
                elif task_name == "medical":
                    medical_data = task_result
        
        # 3. AI Advice combining all data
        if request.include_ai_advice:
            nutrition_info = nutrition_data.get('foods', [])[:3] if nutrition_data else []
            medical_info = medical_data.get('data', {}).get('articles', [])[:3] if medical_data else []
            
            ai_prompt = f"""
            Provide health recommendations for: {request.query}
            
            Nutrition Info: {nutrition_info}
            Medical Research: {medical_info}
            
            Provide:
            1. Nutritional benefits
            2. Health considerations
            3. Recommended intake
            4. Potential interactions
            5. Overall health advice
            """
            
            ai_response = await ai_router.route(ai_prompt)
            results["ai_advice"] = ai_response.get("response")
            results["ai_source"] = ai_response.get("source")
        
        return {
            "success": True,
            "query": request.query,
            "nutrition": nutrition_data,
            "medical": medical_data,
            **results,
            "errors": errors if errors else None
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/location/complete")
async def get_location_complete_info(
    location: str = Query(..., description="City or address"),
    include_weather: bool = Query(True),
    include_news: bool = Query(True),
    include_restaurants: bool = Query(False)
):
    """
    Get complete location information in one call
    
    Combines: Geocoding + Weather + News + (optional) Restaurants
    """
    try:
        tasks = []
        
        # All calls in parallel
        tasks.append(("geocoding", geocoding_router.geocode(location)))
        
        # Weather will be handled after geocoding
        weather_data = None
        
        if include_news:
            tasks.append(("news", news_router.search(location, language="en")))
        
        # Execute all in parallel
        task_results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        results = {}
        geocoding_result = None
        
        for i, (task_name, task_result) in enumerate(zip([t[0] for t in tasks], task_results)):
            if not isinstance(task_result, Exception):
                results[task_name] = task_result
                if task_name == "geocoding":
                    geocoding_result = task_result
        
        # Get weather if geocoding succeeded
        if include_weather and geocoding_result:
            try:
                lat = geocoding_result.get('latitude')
                lon = geocoding_result.get('longitude')
                if lat and lon:
                    weather_data = await weather_router.get_current_weather(lat, lon)
                    results["weather"] = weather_data
            except Exception as e:
                pass
        
        return {
            "success": True,
            "location": location,
            **results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/crypto/complete")
async def get_crypto_complete_info(
    coin_id: str = Query(..., description="Crypto coin ID (bitcoin, ethereum, etc.)"),
    include_news: bool = Query(True),
    include_ai_analysis: bool = Query(True)
):
    """
    Get complete crypto information in one call
    
    Combines: Price + News + AI Analysis
    """
    try:
        tasks = []
        
        # Get price and news in parallel
        tasks.append(("price", coingecko.get_crypto_price(coin_id)))
        
        if include_news:
            tasks.append(("news", news_router.search(coin_id, language="en")))
        
        task_results = await asyncio.gather(*[task[1] for task in tasks], return_exceptions=True)
        
        price_data = None
        news_data = None
        
        for i, (task_name, task_result) in enumerate(zip([t[0] for t in tasks], task_results)):
            if not isinstance(task_result, Exception):
                if task_name == "price":
                    price_data = task_result
                elif task_name == "news":
                    news_data = task_result
        
        results = {
            "price": price_data,
            "news": news_data
        }
        
        # AI Analysis if requested
        if include_ai_analysis and price_data:
            # Extract price from CoinGecko response format
            coin_data = price_data.get(coin_id, {}) if isinstance(price_data, dict) else {}
            price = coin_data.get('usd', 'N/A') if coin_data else 'N/A'
            change_24h = coin_data.get('usd_24h_change', 'N/A') if coin_data else 'N/A'
            market_cap = coin_data.get('usd_market_cap', 'N/A') if coin_data else 'N/A'
            
            news_info = news_data.get('articles', [])[:3] if news_data else []
            
            ai_prompt = f"""
            Analyze {coin_id} cryptocurrency:
            
            Current Price: ${price}
            Change 24h: {change_24h}%
            Market Cap: ${market_cap}
            Recent News: {news_info}
            
            Provide brief analysis and outlook.
            """
            
            ai_response = await ai_router.route(ai_prompt)
            results["ai_analysis"] = ai_response.get("response")
            results["ai_source"] = ai_response.get("source")
        
        return {
            "success": True,
            "coin_id": coin_id,
            **results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

