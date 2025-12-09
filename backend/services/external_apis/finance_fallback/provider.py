"""
Finance Fallback Provider
API de fallback avec données statiques et cache pour garantir la disponibilité
"""
import os
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)


class FinanceFallbackProvider:
    """
    Provider de fallback avec données statiques et cache
    Garantit toujours une réponse même si toutes les APIs externes échouent
    """
    
    def __init__(self):
        self.available = True
        self.cache_dir = Path("data/finance_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Données statiques de référence (dernières valeurs connues)
        self.static_data = self._load_static_data()
        
        logger.info("[OK] Finance Fallback Provider initialized")
    
    def _load_static_data(self) -> Dict[str, Any]:
        """Charger les données statiques de référence"""
        static_file = self.cache_dir / "static_data.json"
        
        # Données par défaut si le fichier n'existe pas
        default_data = {
            "stocks": {
                "AAPL": {"price": 175.00, "change": 0.0, "change_percent": 0.0, "name": "Apple Inc."},
                "MSFT": {"price": 380.00, "change": 0.0, "change_percent": 0.0, "name": "Microsoft Corporation"},
                "TSLA": {"price": 250.00, "change": 0.0, "change_percent": 0.0, "name": "Tesla Inc."},
                "QQQ": {"price": 380.00, "change": 0.0, "change_percent": 0.0, "name": "Invesco QQQ Trust"},
                "SPY": {"price": 450.00, "change": 0.0, "change_percent": 0.0, "name": "SPDR S&P 500 ETF"},
                "DIA": {"price": 350.00, "change": 0.0, "change_percent": 0.0, "name": "SPDR Dow Jones Industrial Average ETF"},
            },
            "crypto": {
                "bitcoin": {"price": 43000.00, "change": 0.0, "change_percent": 0.0, "symbol": "BTC"},
                "ethereum": {"price": 2500.00, "change": 0.0, "change_percent": 0.0, "symbol": "ETH"},
                "btc": {"price": 43000.00, "change": 0.0, "change_percent": 0.0, "symbol": "BTC"},
                "eth": {"price": 2500.00, "change": 0.0, "change_percent": 0.0, "symbol": "ETH"},
            },
            "indices": {
                "S&P 500": {"price": 4500.00, "change": 0.0, "change_percent": 0.0},
                "Dow Jones": {"price": 35000.00, "change": 0.0, "change_percent": 0.0},
                "NASDAQ": {"price": 14000.00, "change": 0.0, "change_percent": 0.0},
            },
            "last_updated": None
        }
        
        if static_file.exists():
            try:
                with open(static_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Vérifier que les données ne sont pas trop anciennes (max 7 jours)
                    last_updated = data.get("last_updated")
                    if last_updated:
                        last_date = datetime.fromisoformat(last_updated)
                        if datetime.now() - last_date < timedelta(days=7):
                            return data
            except Exception as e:
                logger.warning(f"Failed to load static data: {e}")
        
        return default_data
    
    def _save_static_data(self, data: Dict[str, Any]):
        """Sauvegarder les données statiques"""
        static_file = self.cache_dir / "static_data.json"
        data["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(static_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.warning(f"Failed to save static data: {e}")
    
    def _get_cached_data(self, key: str, max_age_hours: int = 24) -> Optional[Dict[str, Any]]:
        """Récupérer des données du cache"""
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                cached = json.load(f)
                
            # Vérifier l'âge du cache
            cached_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
            age = datetime.now() - cached_time
            
            if age < timedelta(hours=max_age_hours):
                return cached.get("data")
            else:
                # Cache expiré
                return None
        except Exception as e:
            logger.debug(f"Failed to read cache for {key}: {e}")
            return None
    
    def _save_to_cache(self, key: str, data: Dict[str, Any]):
        """Sauvegarder des données dans le cache"""
        cache_file = self.cache_dir / f"{key}.json"
        
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.debug(f"Failed to save cache for {key}: {e}")
    
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get stock information from cache or static data"""
        symbol_upper = symbol.upper()
        
        # Vérifier le cache d'abord
        cached = self._get_cached_data(f"stock_{symbol_upper}", max_age_hours=1)
        if cached:
            logger.debug(f"Using cached data for {symbol_upper}")
            return cached
        
        # Utiliser les données statiques
        if symbol_upper in self.static_data.get("stocks", {}):
            stock_data = self.static_data["stocks"][symbol_upper].copy()
            stock_data["symbol"] = symbol_upper
            stock_data["source"] = "fallback_static"
            stock_data["note"] = "Données de référence (dernières valeurs connues)"
            
            # Sauvegarder dans le cache
            self._save_to_cache(f"stock_{symbol_upper}", stock_data)
            
            return stock_data
        
        # Données par défaut si symbol inconnu
        return {
            "symbol": symbol_upper,
            "price": 100.00,
            "change": 0.0,
            "change_percent": 0.0,
            "volume": None,
            "market_cap": None,
            "company_name": symbol_upper,
            "source": "fallback_default",
            "note": "Données par défaut - symbol non reconnu"
        }
    
    async def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary from cache or static data"""
        # Vérifier le cache
        cached = self._get_cached_data("market_summary", max_age_hours=1)
        if cached:
            logger.debug("Using cached market summary")
            return cached
        
        # Utiliser les données statiques
        summary = {}
        indices_data = self.static_data.get("indices", {})
        
        for name, data in indices_data.items():
            summary[name] = {
                "price": data.get("price", 0),
                "change": data.get("change", 0),
                "change_percent": data.get("change_percent", 0),
                "source": "fallback_static",
                "note": "Données de référence"
            }
        
        if summary:
            summary["_meta"] = {
                "source": "fallback_static",
                "note": "Données de référence (dernières valeurs connues)",
                "last_updated": self.static_data.get("last_updated")
            }
            
            # Sauvegarder dans le cache
            self._save_to_cache("market_summary", summary)
        
        return summary
    
    async def get_crypto_price(self, coin_id: str, vs_currency: str = "usd") -> Dict[str, Any]:
        """Get crypto price from cache or static data"""
        coin_lower = coin_id.lower()
        
        # Vérifier le cache
        cached = self._get_cached_data(f"crypto_{coin_lower}", max_age_hours=1)
        if cached:
            logger.debug(f"Using cached data for {coin_lower}")
            return cached
        
        # Utiliser les données statiques
        if coin_lower in self.static_data.get("crypto", {}):
            crypto_data = self.static_data["crypto"][coin_lower].copy()
            price = crypto_data.get("price", 0)
            
            result = {
                coin_lower: {
                    "usd": price,
                    "usd_24h_change": crypto_data.get("change_percent", 0),
                    "source": "fallback_static",
                    "note": "Données de référence"
                }
            }
            
            # Sauvegarder dans le cache
            self._save_to_cache(f"crypto_{coin_lower}", result)
            
            return result
        
        # Données par défaut
        return {
            coin_lower: {
                "usd": 1000.0,
                "usd_24h_change": 0.0,
                "source": "fallback_default",
                "note": "Données par défaut"
            }
        }
    
    def update_from_external(self, data_type: str, key: str, data: Dict[str, Any]):
        """
        Mettre à jour les données statiques depuis une source externe
        Appelé quand une API externe réussit
        """
        if data_type == "stock" and "stocks" in self.static_data:
            self.static_data["stocks"][key.upper()] = {
                "price": data.get("price", 0),
                "change": data.get("change", 0),
                "change_percent": data.get("change_percent", 0),
                "name": data.get("company_name", key)
            }
            self._save_static_data(self.static_data)
            self._save_to_cache(f"stock_{key.upper()}", data)
        
        elif data_type == "crypto" and "crypto" in self.static_data:
            coin_id = key.lower()
            price = data.get("usd") or data.get("price", 0)
            self.static_data["crypto"][coin_id] = {
                "price": price,
                "change": 0,
                "change_percent": data.get("usd_24h_change", 0),
                "symbol": coin_id.upper()[:3]
            }
            self._save_static_data(self.static_data)
            self._save_to_cache(f"crypto_{coin_id}", data)
        
        elif data_type == "market" and "indices" in self.static_data:
            for name, index_data in data.items():
                if name in self.static_data["indices"]:
                    self.static_data["indices"][name] = {
                        "price": index_data.get("price", 0),
                        "change": index_data.get("change", 0),
                        "change_percent": index_data.get("change_percent", 0)
                    }
            self._save_static_data(self.static_data)
            self._save_to_cache("market_summary", data)


# Singleton instance
finance_fallback = FinanceFallbackProvider()

