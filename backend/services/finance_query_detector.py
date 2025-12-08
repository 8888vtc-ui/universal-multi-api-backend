"""
Finance Query Detector
Intelligently detects the type of financial query (crypto, stock, market, currency)
"""
import re
from typing import Dict, Optional, List, Tuple


class FinanceQueryDetector:
    """Detects the type of financial query and extracts relevant symbols"""
    
    # Crypto keywords and symbols
    CRYPTO_KEYWORDS = [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
        "binance", "bnb", "solana", "sol", "cardano", "ada", "polkadot",
        "dogecoin", "doge", "ripple", "xrp", "litecoin", "ltc", "chainlink",
        "link", "uniswap", "uni", "avalanche", "avax", "polygon", "matic"
    ]
    
    # Stock keywords and common symbols
    STOCK_KEYWORDS = [
        "stock", "action", "bourse", "nasdaq", "nyse", "s&p", "sp500",
        "dow jones", "dow", "apple", "microsoft", "google", "amazon",
        "tesla", "meta", "facebook", "netflix", "nvidia", "amd", "intel",
        "invest", "investment", "investir", "investissement", "best", "meilleur",
        "qqq", "spy", "dia", "etf", "index", "indice",
        "produit financier", "financial product", "produit", "product",
        "placement", "investment product", "produit d'investissement"
    ]
    
    # Stock symbol mappings (company name -> symbol)
    STOCK_SYMBOLS = {
        "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL", "amazon": "AMZN",
        "tesla": "TSLA", "meta": "META", "facebook": "META", "netflix": "NFLX",
        "nvidia": "NVDA", "amd": "AMD", "intel": "INTC", "oracle": "ORCL",
        "cisco": "CSCO", "adobe": "ADBE", "salesforce": "CRM", "paypal": "PYPL",
        "visa": "V", "mastercard": "MA", "jpmorgan": "JPM", "bank of america": "BAC",
        "goldman sachs": "GS", "morgan stanley": "MS", "berkshire": "BRK.A",
        "walmart": "WMT", "target": "TGT", "costco": "COST", "home depot": "HD",
        "disney": "DIS", "comcast": "CMCSA", "verizon": "VZ", "at&t": "T"
    }
    
    # Market/indices keywords
    MARKET_KEYWORDS = [
        "marché", "market", "bourse", "indices", "indice", "indices boursiers",
        "wall street", "s&p 500", "sp500", "nasdaq composite", "dow jones",
        "stock market", "marché boursier", "marchés", "markets"
    ]
    
    # Currency keywords
    CURRENCY_KEYWORDS = [
        "euro", "eur", "dollar", "usd", "livre", "gbp", "yen", "jpy",
        "franc suisse", "chf", "yuan", "cny", "devise", "currency", "taux de change"
    ]
    
    @classmethod
    def detect_query_type(cls, query: str) -> Dict[str, any]:
        """
        Detect the type of financial query and extract relevant information
        
        Returns:
            {
                "type": "crypto" | "stock" | "market" | "currency" | "general",
                "symbol": extracted symbol (if applicable),
                "coin_id": crypto coin ID (if applicable),
                "confidence": float (0.0-1.0)
            }
        """
        query_lower = query.lower().strip()
        
        # Check for crypto
        crypto_match = cls._detect_crypto(query_lower)
        if crypto_match:
            return crypto_match
        
        # Check for stock
        stock_match = cls._detect_stock(query_lower)
        if stock_match:
            return stock_match
        
        # Check for market/indices
        market_match = cls._detect_market(query_lower)
        if market_match:
            return market_match
        
        # Check for currency
        currency_match = cls._detect_currency(query_lower)
        if currency_match:
            return currency_match
        
        # Default to general
        return {
            "type": "general",
            "symbol": None,
            "coin_id": None,
            "confidence": 0.3
        }
    
    @classmethod
    def _detect_crypto(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about cryptocurrency"""
        # Check for crypto keywords
        for keyword in cls.CRYPTO_KEYWORDS:
            if keyword in query_lower:
                # Extract coin ID
                coin_id = cls._extract_crypto_id(query_lower, keyword)
                confidence = 0.9 if coin_id else 0.7
                return {
                    "type": "crypto",
                    "symbol": keyword.upper() if len(keyword) <= 5 else None,
                    "coin_id": coin_id,
                    "confidence": confidence
                }
        
        return None
    
    @classmethod
    def _extract_crypto_id(cls, query_lower: str, keyword: str) -> Optional[str]:
        """Extract crypto coin ID from query"""
        # Mapping common names to CoinGecko IDs
        crypto_id_map = {
            "bitcoin": "bitcoin", "btc": "bitcoin",
            "ethereum": "ethereum", "eth": "ethereum",
            "binance": "binancecoin", "bnb": "binancecoin",
            "solana": "solana", "sol": "solana",
            "cardano": "cardano", "ada": "cardano",
            "polkadot": "polkadot",
            "dogecoin": "dogecoin", "doge": "dogecoin",
            "ripple": "ripple", "xrp": "ripple",
            "litecoin": "litecoin", "ltc": "litecoin",
            "chainlink": "chainlink", "link": "chainlink",
            "uniswap": "uniswap", "uni": "uniswap",
            "avalanche": "avalanche", "avax": "avalanche",
            "polygon": "polygon", "matic": "polygon"
        }
        
        # Try exact match first
        if keyword in crypto_id_map:
            return crypto_id_map[keyword]
        
        # Try to find in query
        for name, coin_id in crypto_id_map.items():
            if name in query_lower:
                return coin_id
        
        return keyword  # Fallback to keyword itself
    
    @classmethod
    def _detect_stock(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about stocks"""
        # Check for stock keywords
        for keyword in cls.STOCK_KEYWORDS:
            if keyword in query_lower:
                # Extract stock symbol
                symbol = cls._extract_stock_symbol(query_lower, keyword)
                confidence = 0.9 if symbol else 0.7
                return {
                    "type": "stock",
                    "symbol": symbol,
                    "coin_id": None,
                    "confidence": confidence
                }
        
        # Check for stock symbol pattern (3-5 uppercase letters)
        symbol_pattern = r'\b([A-Z]{2,5})\b'
        matches = re.findall(symbol_pattern, query_lower.upper())
        if matches:
            # Filter out common words that might match
            common_words = {"THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "ITS", "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WHO", "WAY", "USE", "MAN", "YEAR"}
            for match in matches:
                if match not in common_words and len(match) >= 2:
                    return {
                        "type": "stock",
                        "symbol": match,
                        "coin_id": None,
                        "confidence": 0.8
                    }
        
        return None
    
    @classmethod
    def _extract_stock_symbol(cls, query_lower: str, keyword: str) -> Optional[str]:
        """Extract stock symbol from query"""
        # Check symbol mapping
        for name, symbol in cls.STOCK_SYMBOLS.items():
            if name in query_lower:
                return symbol
        
        # Special cases
        if "nasdaq" in query_lower:
            return "QQQ"  # NASDAQ ETF
        elif "s&p" in query_lower or "sp500" in query_lower or "sp 500" in query_lower:
            return "SPY"  # S&P 500 ETF
        elif "dow" in query_lower or "dow jones" in query_lower:
            return "DIA"  # Dow Jones ETF
        
        return None
    
    @classmethod
    def _detect_market(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about market/indices"""
        for keyword in cls.MARKET_KEYWORDS:
            if keyword in query_lower:
                return {
                    "type": "market",
                    "symbol": None,
                    "coin_id": None,
                    "confidence": 0.85
                }
        
        return None
    
    @classmethod
    def _detect_currency(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about currency exchange"""
        for keyword in cls.CURRENCY_KEYWORDS:
            if keyword in query_lower:
                return {
                    "type": "currency",
                    "symbol": None,
                    "coin_id": None,
                    "confidence": 0.8
                }
        
        return None
    
    @classmethod
    def get_recommended_apis(cls, query_type: str, symbol: Optional[str] = None, coin_id: Optional[str] = None) -> List[str]:
        """
        Get recommended API endpoints based on query type
        
        Returns list of API names to call
        """
        if query_type == "crypto":
            apis = ["finance", "coincap"]
            if coin_id:
                apis.append("finance")  # Will use crypto price endpoint
            apis.append("news")  # Financial news
            return apis[:3]  # Limit to 3
        
        elif query_type == "stock":
            apis = ["finance_stock"]  # Stock quote
            if symbol:
                apis.append("finance_company")  # Company profile
                apis.append("finance_news")  # Stock news
            else:
                apis.append("finance_market_news")  # General market news
            return apis[:3]
        
        elif query_type == "market":
            apis = ["finance_market_news", "finance"]  # Market summary + news
            apis.append("news")  # General news
            return apis[:3]
        
        elif query_type == "currency":
            apis = ["exchange", "news"]  # Exchange rates + news
            return apis[:2]
        
        else:  # general
            # Pour les questions générales, récupérer des données de marché pour enrichir la réponse
            # Essayer d'abord les actualités marché, puis les actualités générales
            apis = ["finance_market_news", "news"]  # Actualités marché + générales
            return apis[:2]


Intelligently detects the type of financial query (crypto, stock, market, currency)
"""
import re
from typing import Dict, Optional, List, Tuple


class FinanceQueryDetector:
    """Detects the type of financial query and extracts relevant symbols"""
    
    # Crypto keywords and symbols
    CRYPTO_KEYWORDS = [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
        "binance", "bnb", "solana", "sol", "cardano", "ada", "polkadot",
        "dogecoin", "doge", "ripple", "xrp", "litecoin", "ltc", "chainlink",
        "link", "uniswap", "uni", "avalanche", "avax", "polygon", "matic"
    ]
    
    # Stock keywords and common symbols
    STOCK_KEYWORDS = [
        "stock", "action", "bourse", "nasdaq", "nyse", "s&p", "sp500",
        "dow jones", "dow", "apple", "microsoft", "google", "amazon",
        "tesla", "meta", "facebook", "netflix", "nvidia", "amd", "intel",
        "invest", "investment", "investir", "investissement", "best", "meilleur",
        "qqq", "spy", "dia", "etf", "index", "indice",
        "produit financier", "financial product", "produit", "product",
        "placement", "investment product", "produit d'investissement"
    ]
    
    # Stock symbol mappings (company name -> symbol)
    STOCK_SYMBOLS = {
        "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL", "amazon": "AMZN",
        "tesla": "TSLA", "meta": "META", "facebook": "META", "netflix": "NFLX",
        "nvidia": "NVDA", "amd": "AMD", "intel": "INTC", "oracle": "ORCL",
        "cisco": "CSCO", "adobe": "ADBE", "salesforce": "CRM", "paypal": "PYPL",
        "visa": "V", "mastercard": "MA", "jpmorgan": "JPM", "bank of america": "BAC",
        "goldman sachs": "GS", "morgan stanley": "MS", "berkshire": "BRK.A",
        "walmart": "WMT", "target": "TGT", "costco": "COST", "home depot": "HD",
        "disney": "DIS", "comcast": "CMCSA", "verizon": "VZ", "at&t": "T"
    }
    
    # Market/indices keywords
    MARKET_KEYWORDS = [
        "marché", "market", "bourse", "indices", "indice", "indices boursiers",
        "wall street", "s&p 500", "sp500", "nasdaq composite", "dow jones",
        "stock market", "marché boursier", "marchés", "markets"
    ]
    
    # Currency keywords
    CURRENCY_KEYWORDS = [
        "euro", "eur", "dollar", "usd", "livre", "gbp", "yen", "jpy",
        "franc suisse", "chf", "yuan", "cny", "devise", "currency", "taux de change"
    ]
    
    @classmethod
    def detect_query_type(cls, query: str) -> Dict[str, any]:
        """
        Detect the type of financial query and extract relevant information
        
        Returns:
            {
                "type": "crypto" | "stock" | "market" | "currency" | "general",
                "symbol": extracted symbol (if applicable),
                "coin_id": crypto coin ID (if applicable),
                "confidence": float (0.0-1.0)
            }
        """
        query_lower = query.lower().strip()
        
        # Check for crypto
        crypto_match = cls._detect_crypto(query_lower)
        if crypto_match:
            return crypto_match
        
        # Check for stock
        stock_match = cls._detect_stock(query_lower)
        if stock_match:
            return stock_match
        
        # Check for market/indices
        market_match = cls._detect_market(query_lower)
        if market_match:
            return market_match
        
        # Check for currency
        currency_match = cls._detect_currency(query_lower)
        if currency_match:
            return currency_match
        
        # Default to general
        return {
            "type": "general",
            "symbol": None,
            "coin_id": None,
            "confidence": 0.3
        }
    
    @classmethod
    def _detect_crypto(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about cryptocurrency"""
        # Check for crypto keywords
        for keyword in cls.CRYPTO_KEYWORDS:
            if keyword in query_lower:
                # Extract coin ID
                coin_id = cls._extract_crypto_id(query_lower, keyword)
                confidence = 0.9 if coin_id else 0.7
                return {
                    "type": "crypto",
                    "symbol": keyword.upper() if len(keyword) <= 5 else None,
                    "coin_id": coin_id,
                    "confidence": confidence
                }
        
        return None
    
    @classmethod
    def _extract_crypto_id(cls, query_lower: str, keyword: str) -> Optional[str]:
        """Extract crypto coin ID from query"""
        # Mapping common names to CoinGecko IDs
        crypto_id_map = {
            "bitcoin": "bitcoin", "btc": "bitcoin",
            "ethereum": "ethereum", "eth": "ethereum",
            "binance": "binancecoin", "bnb": "binancecoin",
            "solana": "solana", "sol": "solana",
            "cardano": "cardano", "ada": "cardano",
            "polkadot": "polkadot",
            "dogecoin": "dogecoin", "doge": "dogecoin",
            "ripple": "ripple", "xrp": "ripple",
            "litecoin": "litecoin", "ltc": "litecoin",
            "chainlink": "chainlink", "link": "chainlink",
            "uniswap": "uniswap", "uni": "uniswap",
            "avalanche": "avalanche", "avax": "avalanche",
            "polygon": "polygon", "matic": "polygon"
        }
        
        # Try exact match first
        if keyword in crypto_id_map:
            return crypto_id_map[keyword]
        
        # Try to find in query
        for name, coin_id in crypto_id_map.items():
            if name in query_lower:
                return coin_id
        
        return keyword  # Fallback to keyword itself
    
    @classmethod
    def _detect_stock(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about stocks"""
        # Check for stock keywords
        for keyword in cls.STOCK_KEYWORDS:
            if keyword in query_lower:
                # Extract stock symbol
                symbol = cls._extract_stock_symbol(query_lower, keyword)
                confidence = 0.9 if symbol else 0.7
                return {
                    "type": "stock",
                    "symbol": symbol,
                    "coin_id": None,
                    "confidence": confidence
                }
        
        # Check for stock symbol pattern (3-5 uppercase letters)
        symbol_pattern = r'\b([A-Z]{2,5})\b'
        matches = re.findall(symbol_pattern, query_lower.upper())
        if matches:
            # Filter out common words that might match
            common_words = {"THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET", "HAS", "HIM", "HIS", "HOW", "ITS", "MAY", "NEW", "NOW", "OLD", "SEE", "TWO", "WHO", "WAY", "USE", "MAN", "YEAR"}
            for match in matches:
                if match not in common_words and len(match) >= 2:
                    return {
                        "type": "stock",
                        "symbol": match,
                        "coin_id": None,
                        "confidence": 0.8
                    }
        
        return None
    
    @classmethod
    def _extract_stock_symbol(cls, query_lower: str, keyword: str) -> Optional[str]:
        """Extract stock symbol from query"""
        # Check symbol mapping
        for name, symbol in cls.STOCK_SYMBOLS.items():
            if name in query_lower:
                return symbol
        
        # Special cases
        if "nasdaq" in query_lower:
            return "QQQ"  # NASDAQ ETF
        elif "s&p" in query_lower or "sp500" in query_lower or "sp 500" in query_lower:
            return "SPY"  # S&P 500 ETF
        elif "dow" in query_lower or "dow jones" in query_lower:
            return "DIA"  # Dow Jones ETF
        
        return None
    
    @classmethod
    def _detect_market(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about market/indices"""
        for keyword in cls.MARKET_KEYWORDS:
            if keyword in query_lower:
                return {
                    "type": "market",
                    "symbol": None,
                    "coin_id": None,
                    "confidence": 0.85
                }
        
        return None
    
    @classmethod
    def _detect_currency(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about currency exchange"""
        for keyword in cls.CURRENCY_KEYWORDS:
            if keyword in query_lower:
                return {
                    "type": "currency",
                    "symbol": None,
                    "coin_id": None,
                    "confidence": 0.8
                }
        
        return None
    
    @classmethod
    def get_recommended_apis(cls, query_type: str, symbol: Optional[str] = None, coin_id: Optional[str] = None) -> List[str]:
        """
        Get recommended API endpoints based on query type
        
        Returns list of API names to call
        """
        if query_type == "crypto":
            apis = ["finance", "coincap"]
            if coin_id:
                apis.append("finance")  # Will use crypto price endpoint
            apis.append("news")  # Financial news
            return apis[:3]  # Limit to 3
        
        elif query_type == "stock":
            apis = ["finance_stock"]  # Stock quote
            if symbol:
                apis.append("finance_company")  # Company profile
                apis.append("finance_news")  # Stock news
            else:
                apis.append("finance_market_news")  # General market news
            return apis[:3]
        
        elif query_type == "market":
            apis = ["finance_market_news", "finance"]  # Market summary + news
            apis.append("news")  # General news
            return apis[:3]
        
        elif query_type == "currency":
            apis = ["exchange", "news"]  # Exchange rates + news
            return apis[:2]
        
        else:  # general
            # Pour les questions générales, récupérer des données de marché pour enrichir la réponse
            # Essayer d'abord les actualités marché, puis les actualités générales
            apis = ["finance_market_news", "news"]  # Actualités marché + générales
            return apis[:2]

