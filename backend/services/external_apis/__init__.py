"""
External APIs Package
Finance, Medical, Entertainment providers
"""
from .finance import coingecko, alphavantage, yahoo_finance
from .medical import pubmed, openfda
from .entertainment import tmdb, yelp, spotify

__all__ = [
    # Finance
    'coingecko',
    'alphavantage',
    'yahoo_finance',
    # Medical
    'pubmed',
    'openfda',
    # Entertainment
    'tmdb',
    'yelp',
    'spotify'
]

    polygon = None

try:
    from .finance_fallback.provider import finance_fallback
except ImportError:
    finance_fallback = None

__all__ = [
    # Finance
    'coingecko',
    'alphavantage',
    'yahoo_finance',
    'finnhub',
    'twelve_data',
    'polygon',
    'finance_fallback',
    # Medical
    'pubmed',
    'openfda',
    # Entertainment
    'tmdb',
    'yelp',
    'spotify'
]
