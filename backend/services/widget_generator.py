"""
Widget Generator
Transforms raw API data into structured UI widgets (Charts, Cards, Lists)
"""
from typing import Dict, List, Any, Optional
from models.schemas import WidgetData

def generate_widgets_from_data(expert_id: str, raw_data: Dict[str, Any]) -> List[WidgetData]:
    """
    Generate appropriate widgets based on expert type and available data
    """
    widgets = []
    
    if not raw_data:
        return []
    
    # 1. FINANCE WIDGETS
    if expert_id == "finance":
        # Crypto Card
        if "bit" in str(raw_data).lower() or "coin" in str(raw_data).lower():
            for key, val in raw_data.items():
                if isinstance(val, dict) and "price" in str(val).lower():
                    widgets.append(WidgetData(
                        type="crypto_card",
                        title=val.get("name", "Crypto"),
                        data={
                            "symbol": val.get("symbol", ""),
                            "price": float(val.get("priceUsd", 0) or val.get("current_price", 0)),
                            "change_24h": float(val.get("changePercent24Hr", 0) or val.get("price_change_24h", 0)),
                            "market_cap": float(val.get("marketCapUsd", 0) or val.get("market_cap", 0))
                        }
                    ))
    
    # 2. NEWS WIDGETS
    elif expert_id == "news":
        articles = raw_data.get("articles", [])
        if articles:
            # News List Widget
            widgets.append(WidgetData(
                type="news_list",
                title="Dernières Actualités",
                data={
                    "items": [
                        {
                            "title": a.get("title"),
                            "source": a.get("source", {}).get("name", "Inconnu"),
                            "url": a.get("url"),
                            "image": a.get("urlToImage"),
                            "time": a.get("publishedAt")
                        }
                        for a in articles[:5]  # Limit to 5
                    ]
                }
            ))

    # 3. WEATHER WIDGETS
    elif expert_id == "weather":
        if "temperature" in raw_data or "temp" in str(raw_data):
            # Weather Card
            temp = raw_data.get("temperature") or raw_data.get("temp")
            widgets.append(WidgetData(
                type="weather_card",
                title=f"Météo à {raw_data.get('location', 'Unknown')}",
                data={
                    "location": raw_data.get("location"),
                    "temperature": temp,
                    "condition": raw_data.get("description") or raw_data.get("weather_code"),
                    "wind": raw_data.get("windspeed"),
                    "humidity": raw_data.get("humidity")
                }
            ))
            
    return widgets
