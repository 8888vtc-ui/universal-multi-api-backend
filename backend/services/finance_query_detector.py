"""
Finance Query Detector
Intelligently detects the type of financial query (crypto, stock, market, forex)
"""
import re
from typing import Dict, Optional, List


class FinanceQueryDetector:
    """Detects the type of financial query and extracts relevant symbols"""
    
    # Crypto keywords and symbols
    CRYPTO_KEYWORDS = [
        "bitcoin", "btc", "ethereum", "eth", "crypto", "cryptocurrency",
        "binance", "bnb", "solana", "sol", "cardano", "ada", "polkadot",
        "dogecoin", "doge", "ripple", "xrp", "litecoin", "ltc", "chainlink",
        "link", "uniswap", "uni", "avalanche", "avax", "polygon", "matic",
        "coin", "token", "defi", "nft", "altcoin", "stablecoin"
    ]
    
    # Stock keywords and common symbols
    STOCK_KEYWORDS = [
        "stock", "action", "nasdaq", "nyse", "apple", "microsoft", "google", "amazon",
        "tesla", "meta", "facebook", "netflix", "nvidia", "amd", "intel",
        "invest", "investment", "investir", "investissement",
        "qqq", "spy", "dia", "etf", "share", "shares", "equity"
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
        "stock market", "marché boursier", "marchés", "markets", "cac", "cac40",
        "dax", "ftse", "nikkei"
    ]
    
    # Forex keywords
    FOREX_KEYWORDS = [
        "eur/usd", "usd/eur", "gbp/usd", "usd/jpy", "forex", "fx",
        "taux de change", "exchange rate", "change", "devise", "currency",
        "euro", "dollar", "livre", "yen", "franc suisse", "chf",
        "eur", "usd", "gbp", "jpy", "cad", "aud", "nzd"
    ]
    
    # Crypto ID mapping
    CRYPTO_ID_MAP = {
        "bitcoin": "bitcoin", "btc": "bitcoin",
        "ethereum": "ethereum", "eth": "ethereum",
        "binance": "binancecoin", "bnb": "binancecoin",
        "solana": "solana", "sol": "solana",
        "cardano": "cardano", "ada": "cardano",
        "polkadot": "polkadot", "dot": "polkadot",
        "dogecoin": "dogecoin", "doge": "dogecoin",
        "ripple": "ripple", "xrp": "ripple",
        "litecoin": "litecoin", "ltc": "litecoin",
        "chainlink": "chainlink", "link": "chainlink",
        "uniswap": "uniswap", "uni": "uniswap",
        "avalanche": "avalanche-2", "avax": "avalanche-2",
        "polygon": "matic-network", "matic": "matic-network"
    }
    
    # Fallback messages par type
    FALLBACK_MESSAGES = {
        "stock": "Aucune donnée boursière trouvée pour {symbol}.",
        "crypto": "Aucune donnée crypto trouvée.",
        "forex": "Aucune donnée forex trouvée.",
        "market": "Aucune donnée marché trouvée.",
        "general": "Aucune donnée financière trouvée."
    }
    
    @classmethod
    def detect_query_type(cls, query: str) -> Dict[str, any]:
        """
        Detect the type of financial query and extract relevant information
        
        Returns:
            {
                "type": "crypto" | "stock" | "market" | "forex" | "general",
                "symbol": extracted symbol (if applicable),
                "coin_id": crypto coin ID (if applicable),
                "confidence": float (0.0-1.0)
            }
        """
        query_lower = query.lower().strip()
        
        # Check for crypto first (high priority)
        crypto_match = cls._detect_crypto(query_lower)
        if crypto_match:
            return crypto_match
        
        # Check for forex (before stock to avoid conflicts)
        forex_match = cls._detect_forex(query_lower)
        if forex_match:
            return forex_match
        
        # Check for stock
        stock_match = cls._detect_stock(query_lower)
        if stock_match:
            return stock_match
        
        # Check for market/indices
        market_match = cls._detect_market(query_lower)
        if market_match:
            return market_match
        
        # Check for ticker pattern (2-5 uppercase letters)
        ticker = cls._extract_ticker(query_lower)
        if ticker:
            return {
                "type": "stock",
                "symbol": ticker,
                "coin_id": None,
                "confidence": 0.7
            }
        
        # Default to market (for finance expert, market is better than nothing)
        return {
            "type": "market",
            "symbol": None,
            "coin_id": None,
            "confidence": 0.3
        }
    
    @classmethod
    def _detect_crypto(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about cryptocurrency"""
        for keyword in cls.CRYPTO_KEYWORDS:
            if keyword in query_lower:
                coin_id = cls.CRYPTO_ID_MAP.get(keyword)
                if not coin_id:
                    # Try to find in the full map
                    for name, cid in cls.CRYPTO_ID_MAP.items():
                        if name in query_lower:
                            coin_id = cid
                            break
                
                confidence = 0.9 if coin_id else 0.7
                return {
                    "type": "crypto",
                    "symbol": keyword.upper() if len(keyword) <= 5 else None,
                    "coin_id": coin_id or keyword,
                    "confidence": confidence
                }
        
        return None
    
    @classmethod
    def _detect_forex(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about forex"""
        # Check for currency pair pattern (EUR/USD, etc.)
        pair_pattern = r'([a-z]{3})[/\-]([a-z]{3})'
        pair_match = re.search(pair_pattern, query_lower)
        if pair_match:
            base = pair_match.group(1).upper()
            quote = pair_match.group(2).upper()
            return {
                "type": "forex",
                "symbol": f"{base}/{quote}",
                "coin_id": None,
                "base_currency": base,
                "quote_currency": quote,
                "confidence": 0.95
            }
        
        # Check for forex keywords
        for keyword in cls.FOREX_KEYWORDS:
            if keyword in query_lower:
                return {
                    "type": "forex",
                    "symbol": None,
                    "coin_id": None,
                    "confidence": 0.8
                }
        
        return None
    
    @classmethod
    def _detect_stock(cls, query_lower: str) -> Optional[Dict]:
        """Detect if query is about stocks"""
        # Check company names first
        for name, symbol in cls.STOCK_SYMBOLS.items():
            if name in query_lower:
                return {
                    "type": "stock",
                    "symbol": symbol,
                    "coin_id": None,
                    "confidence": 0.95
                }
        
        # Check for stock keywords
        for keyword in cls.STOCK_KEYWORDS:
            if keyword in query_lower:
                symbol = cls._extract_stock_symbol(query_lower)
                confidence = 0.9 if symbol else 0.7
                return {
                    "type": "stock",
                    "symbol": symbol,
                    "coin_id": None,
                    "confidence": confidence
                }
        
        return None
    
    @classmethod
    def _extract_stock_symbol(cls, query_lower: str) -> Optional[str]:
        """Extract stock symbol from query"""
        # Check company name -> symbol mapping
        for name, symbol in cls.STOCK_SYMBOLS.items():
            if name in query_lower:
                return symbol
        
        # Special indices
        if "nasdaq" in query_lower:
            return "QQQ"
        elif "s&p" in query_lower or "sp500" in query_lower:
            return "SPY"
        elif "dow" in query_lower:
            return "DIA"
        
        return None
    
    @classmethod
    def _extract_ticker(cls, query_lower: str) -> Optional[str]:
        """Extract ticker symbol pattern (2-5 uppercase letters)"""
        symbol_pattern = r'\b([A-Z]{2,5})\b'
        matches = re.findall(symbol_pattern, query_lower.upper())
        
        if matches:
            # Filter out common words
            common_words = {
                "THE", "AND", "FOR", "ARE", "BUT", "NOT", "YOU", "ALL", 
                "CAN", "HER", "WAS", "ONE", "OUR", "OUT", "DAY", "GET",
                "HAS", "HIM", "HIS", "HOW", "ITS", "MAY", "NEW", "NOW",
                "OLD", "SEE", "TWO", "WHO", "WAY", "USE", "MAN", "PRIX",
                "EST", "QUI", "QUE", "LES", "DES", "UNE", "PAR", "SUR"
            }
            for match in matches:
                if match not in common_words and len(match) >= 2:
                    return match
        
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
    def get_recommended_apis(cls, query_type: str, symbol: Optional[str] = None, coin_id: Optional[str] = None) -> List[str]:
        """
        Get recommended API endpoints based on query type
        
        Returns list of API names to call
        """
        if query_type == "crypto":
            # Crypto: prix + news
            apis = ["finance", "coincap", "finance_market_news"]
            return apis[:3]
        
        elif query_type == "stock":
            # Stock: quote + company + news
            apis = ["finance_stock", "finance_company", "finance_news"]
            return apis[:3]
        
        elif query_type == "forex":
            # Forex: exchange rates + news
            apis = ["exchange", "finance_market_news"]
            return apis[:2]
        
        elif query_type == "market":
            # Market: news + general data
            apis = ["finance_market_news", "finance_news"]
            return apis[:2]
        
        else:  # general
            apis = ["finance_market_news", "news"]
            return apis[:2]
    
    @classmethod
    def get_fallback_message(cls, query_type: str, symbol: Optional[str] = None) -> str:
        """Get appropriate fallback message when no data found"""
        message = cls.FALLBACK_MESSAGES.get(query_type, cls.FALLBACK_MESSAGES["general"])
        if symbol and "{symbol}" in message:
            return message.format(symbol=symbol)
        return message.replace(" pour {symbol}", "")


# Test function
def test_detector():
    queries = [
        "Prix du Bitcoin",
        "Cours de l'action Apple",
        "EUR/USD taux de change",
        "Comment va le marché aujourd'hui",
        "What is the price of TSLA"
    ]
    
    for query in queries:
        result = FinanceQueryDetector.detect_query_type(query)
        apis = FinanceQueryDetector.get_recommended_apis(
            result["type"], 
            result.get("symbol"), 
            result.get("coin_id")
        )
        print(f"\nQuery: {query}")
        print(f"Type: {result['type']}, Symbol: {result.get('symbol')}, APIs: {apis}")


if __name__ == "__main__":
    test_detector()
