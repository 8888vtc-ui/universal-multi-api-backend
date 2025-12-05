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
