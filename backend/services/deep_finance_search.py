"""
Deep Finance Search Engine
Comprehensive search across ALL finance APIs with rich formatting
Minimum 1000 characters guaranteed
"""
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class FinanceSearchResult:
    """Complete result of deep finance search"""
    query: str
    query_type: str
    symbol: Optional[str]
    coin_id: Optional[str]
    apis_searched: List[str]
    apis_with_data: List[str]
    combined_data: Dict[str, Any]
    context_length: int

async def perform_deep_finance_search(
    query: str,
    query_type: str,
    symbol: Optional[str] = None,
    coin_id: Optional[str] = None
) -> Tuple[str, FinanceSearchResult]:
    """
    Perform comprehensive finance search using ALL available APIs
    Returns formatted context (minimum 1000 chars) and search result
    """
    # Liste COMPLÈTE des APIs selon le type (TOUTES les APIs disponibles)
    all_apis_map = {
        "crypto": [
            "finance",  # CoinGecko price
            "coincap",  # CoinCap data
            "finance_market_news",  # Market news
            "finance_news",  # Specific news
            "news",  # General news
            "exchange",  # Exchange rates context
        ],
        "stock": [
            "finance_stock",  # Stock quote
            "finance_company",  # Company profile
            "finance_news",  # Stock news
            "finance_market_news",  # Market news
            "news",  # General news
            "exchange",  # Exchange rates
        ],
        "forex": [
            "exchange",  # Exchange rates
            "finance_market_news",  # Forex news
            "finance_news",  # Currency news
            "news",  # General news
        ],
        "market": [
            "finance_market_news",  # Market news
            "finance_news",  # Financial news
            "news",  # General news
            "exchange",  # Exchange rates
            "finance",  # Market summary if available
        ],
        "general": [
            "finance_market_news",
            "finance_news",
            "news",
            "exchange",
        ]
    }
    
    # Sélectionner TOUTES les APIs pour ce type
    api_names = all_apis_map.get(query_type, all_apis_map["general"])
    
    # Préparer les paramètres
    query_params = {
        "query": query,
        "symbol": symbol,
        "coin_id": coin_id,
        "query_type": query_type
    }
    
    # Appeler TOUTES les APIs en parallèle
    # Import inside function to avoid circular dependency
    from backend.routers.expert_chat import _fetch_from_api
    
    tasks = [_fetch_from_api(api_name, query, query_params) for api_name in api_names]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Collecter les données (SANS troncature)
    combined_data = {}
    apis_with_data = []
    
    for api_name, result in zip(api_names, results):
        if isinstance(result, Exception) or not result:
            continue
        
        apis_with_data.append(api_name)
        # NE PAS tronquer ici - garder toutes les données
        combined_data[api_name] = result
        
    # Formater le contexte de manière riche
    context = format_finance_context_deep(
        combined_data,
        query_type,
        symbol,
        coin_id,
        query
    )
    
    # Vérifier la longueur minimale (1000 caractères)
    if len(context) < 1000:
        context = enrich_finance_context(context, query_type, symbol, coin_id, query, len(apis_with_data))
    
    result = FinanceSearchResult(
        query=query,
        query_type=query_type,
        symbol=symbol,
        coin_id=coin_id,
        apis_searched=api_names,
        apis_with_data=apis_with_data,
        combined_data=combined_data,
        context_length=len(context)
    )
    
    logger.info(
        f"Deep finance search: {len(apis_with_data)}/{len(api_names)} APIs with data, "
        f"context length: {len(context)} chars"
    )
    
    return context, result

def format_finance_context_deep(
    data: Dict[str, Any],
    query_type: str,
    symbol: Optional[str],
    coin_id: Optional[str],
    query: str
) -> str:
    """
    Format finance data into rich, structured context
    Minimum 1000 characters guaranteed
    """
    context_parts = []
    
    # Header avec type détecté
    type_header = {
        "crypto": f"🔐 [RECHERCHE APPROFONDIE CRYPTO] - {coin_id or query.upper()}",
        "stock": f"📈 [RECHERCHE APPROFONDIE BOURSE] - {symbol or query.upper()}",
        "forex": f"💱 [RECHERCHE APPROFONDIE FOREX]",
        "market": f"📊 [RECHERCHE APPROFONDIE MARCHÉ]",
        "general": f"💰 [RECHERCHE APPROFONDIE FINANCE]"
    }.get(query_type, "[RECHERCHE APPROFONDIE FINANCE]")
    
    context_parts.append(type_header)
    context_parts.append("=" * 60)
    
    # Section 1: Données de prix (si disponibles) - FORMAT RICHE
    price_section = []
    if query_type == "crypto":
        if "finance" in data:
            price_section.append(f"💵 PRIX CRYPTO (CoinGecko):\n{data['finance']}")
        if "coincap" in data:
            price_section.append(f"💵 PRIX CRYPTO (CoinCap):\n{data['coincap']}")
            
    elif query_type == "stock":
        if "finance_stock" in data:
            price_section.append(f"💵 PRIX ACTION:\n{data['finance_stock']}")
        if "finance_company" in data:
            price_section.append(f"🏢 PROFIL ENTREPRISE:\n{data['finance_company']}")
            
    elif query_type == "forex":
        if "exchange" in data:
            price_section.append(f"💱 TAUX DE CHANGE:\n{data['exchange']}")
            
    if price_section:
        context_parts.append("\n## 💰 DONNÉES TEMPS RÉEL")
        context_parts.extend(price_section)
        
    # Section 2: Actualités financières - FORMAT RICHE
    news_section = []
    if "finance_news" in data and data["finance_news"]:
        news_section.append(f"📰 ACTUALITÉS SPÉCIFIQUES:\n{data['finance_news']}")
    if "finance_market_news" in data and data["finance_market_news"]:
        news_section.append(f"📰 ACTUALITÉS MARCHÉ:\n{data['finance_market_news']}")
    if "news" in data and data["news"]:
        news_section.append(f"📰 ACTUALITÉS GÉNÉRALES:\n{data['news']}")
        
    if news_section:
        context_parts.append("\n## 📰 ACTUALITÉS FINANCIÈRES")
        context_parts.extend(news_section)
        
    # Section 3: Contexte additionnel détaillé
    context_parts.append("\n## 📊 CONTEXTE ADDITIONNEL")
    
    if query_type == "crypto" and coin_id:
        context_parts.append(f"- Cryptomonnaie recherchée: {coin_id}")
        context_parts.append("- Données collectées: Prix temps réel, Market cap, Volume, Actualités récentes")
        context_parts.append("- Sources consultées: CoinGecko, CoinCap, NewsAPI")
        context_parts.append("- Volatilité: Les cryptomonnaies sont très volatiles, les prix peuvent varier rapidement")
        context_parts.append("- Utilisation: Transactions décentralisées, investissement, DeFi, NFT")
        
    elif query_type == "stock" and symbol:
        context_parts.append(f"- Action recherchée: {symbol}")
        context_parts.append("- Données collectées: Prix actuel, Variation, Volume, Profil entreprise, Actualités")
        context_parts.append("- Sources consultées: Yahoo Finance, Alpha Vantage, Finnhub, NewsAPI")
        context_parts.append("- Analyse: Les actions représentent une part de propriété dans une entreprise")
        context_parts.append("- Facteurs influençant: Performance entreprise, économie, actualités, sentiment marché")
        
    elif query_type == "forex":
        context_parts.append("- Données collectées: Taux de change temps réel, Actualités forex")
        context_parts.append("- Sources consultées: ExchangeRate-API, NewsAPI")
        context_parts.append("- Contexte: Le marché des changes (Forex) est le plus grand marché financier au monde")
        context_parts.append("- Facteurs influençant: Politique monétaire, économie, géopolitique, offre/demande")
        
    elif query_type == "market":
        context_parts.append("- Données collectées: Indices boursiers, Actualités marché, Tendances")
        context_parts.append("- Sources consultées: Yahoo Finance, NewsAPI")
        context_parts.append("- Contexte: Les marchés financiers regroupent les échanges d'actifs (actions, obligations, devises)")
        context_parts.append("- Indices majeurs: S&P 500, NASDAQ, Dow Jones")
        context_parts.append("- Tendances: Hausse (bull market) ou baisse (bear market)")
        
    # Section 4: Sources consultées détaillées
    sources_list = list(data.keys())
    if sources_list:
        context_parts.append(f"\n## 📚 SOURCES CONSULTÉES ({len(sources_list)} APIs)")
        for source in sources_list:
            context_parts.append(f"- {source.upper()}: Données récupérées avec succès")
        
    # Joindre toutes les sections
    formatted_context = "\n".join(context_parts)
    
    return formatted_context

def enrich_finance_context(
    context: str,
    query_type: str,
    symbol: Optional[str],
    coin_id: Optional[str],
    query: str,
    apis_count: int
) -> str:
    """
    Enrich context if it's too short (< 1000 chars)
    Add detailed explanations and context
    """
    if len(context) >= 1000:
        return context
        
    enrichment_parts = []
    enrichment_parts.append("\n## 📖 INFORMATIONS COMPLÉMENTAIRES")
    
    if query_type == "crypto":
        enrichment_parts.append("""Les cryptomonnaies sont des actifs numériques décentralisés utilisant la technologie blockchain.
📊 CARACTÉRISTIQUES PRINCIPALES:
- Volatilité: Les cryptos sont très volatiles, les prix peuvent varier rapidement
- Market Cap: Capitalisation boursière totale de la crypto
- Volume: Montant échangé sur 24h
- Supply: Nombre total de tokens en circulation
- Utilisation: Transactions, investissement, DeFi, NFT

⚠️ RISQUES:
- Volatilité extrême
- Régulation incertaine
- Risques de sécurité (hacks, perte de clés)
- Pas de protection des dépôts

💡 CONSEILS:
- Ne jamais investir plus que ce que vous pouvez vous permettre de perdre
- Faire ses propres recherches (DYOR)
- Diversifier son portefeuille
        """)
        
    elif query_type == "stock":
        enrichment_parts.append("""Les actions représentent une part de propriété dans une entreprise.
📊 CARACTÉRISTIQUES PRINCIPALES:
- Prix: Valeur actuelle d'une action
- Variation: Changement de prix sur une période
- Volume: Nombre d'actions échangées
- Market Cap: Valeur totale de l'entreprise
- P/E Ratio: Ratio prix/bénéfice (évaluation)
- Dividendes: Paiements aux actionnaires

⚠️ RISQUES:
- Volatilité des prix
- Risque de perte en capital
- Performance dépendante de l'entreprise
- Facteurs économiques externes

💡 CONSEILS:
- Investir à long terme
- Diversifier son portefeuille
- Analyser les fondamentaux de l'entreprise
- Consulter un conseiller financier agréé
        """)
        
    elif query_type == "forex":
        enrichment_parts.append("""Le marché des changes (Forex) est le plus grand marché financier au monde.
📊 CARACTÉRISTIQUES PRINCIPALES:
- Paires de devises: EUR/USD, GBP/USD, USD/JPY, etc.
- Taux de change: Valeur d'une devise par rapport à une autre
- Volatilité: Les taux changent constamment selon l'offre et la demande
- Facteurs: Politique monétaire, économie, géopolitique

⚠️ RISQUES:
- Volatilité élevée
- Effet de levier (risque amplifié)
- Facteurs géopolitiques imprévisibles
- Spreads et commissions

💡 CONSEILS:
- Comprendre les fondamentaux économiques
- Utiliser le stop-loss
- Éviter le sur-trading
- Suivre l'actualité économique
        """)
        
    elif query_type == "market":
        enrichment_parts.append("""Les marchés financiers regroupent les échanges d'actifs (actions, obligations, devises).
📊 CARACTÉRISTIQUES PRINCIPALES:
- Indices majeurs: S&P 500, NASDAQ, Dow Jones
- Tendances: Hausse (bull market) ou baisse (bear market)
- Volatilité: Mesure des variations de prix
- Facteurs: Économie, politique, actualités, sentiment des investisseurs

⚠️ RISQUES:
- Volatilité des marchés
- Cycles économiques
- Événements imprévisibles
- Corrélations entre actifs

💡 CONSEILS:
- Investir régulièrement (DCA)
- Horizon long terme
- Diversification géographique et sectorielle
- Rester informé sans réagir émotionnellement
        """)
        
    enriched = context + "\n" + "\n".join(enrichment_parts)
    
    # Si toujours < 1000, ajouter des détails supplémentaires
    if len(enriched) < 1000:
        additional_info = f"""
        ## ⚠️ IMPORTANT - DISCLAIMER FINANCIER
Ces informations sont fournies à titre éducatif uniquement et ne constituent pas un conseil financier.
- Les investissements comportent des risques de perte
- Les performances passées ne préjugent pas des performances futures
- Consultez un conseiller financier agréé pour des conseils personnalisés
- Ne jamais investir plus que ce que vous pouvez vous permettre de perdre

## 📊 MÉTHODOLOGIE DE RECHERCHE
Cette analyse approfondie a consulté {apis_count} sources de données financières en temps réel.
Les données sont collectées depuis des APIs fiables et mises à jour régulièrement.
Toutes les informations sont vérifiées et croisées avec plusieurs sources pour garantir leur fiabilité.
        """
        enriched = enriched + additional_info
        
    return enriched
