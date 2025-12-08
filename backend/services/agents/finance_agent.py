"""
Finance Agent with sub-agents (Crypto, Stock, Market, Currency)
"""
import logging
from typing import List, Optional

from .base_agent import ConversationalQualityAgent
from .base_tool import BaseTool
from .tools.finance_tools import (
    CryptoPriceTool,
    StockQuoteTool,
    MarketSummaryTool,
    CurrencyRateTool,
    MarketNewsTool
)
from services.finance_query_detector import FinanceQueryDetector

logger = logging.getLogger(__name__)


class CryptoSubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in cryptocurrency queries"""
    
    def __init__(self):
        tools = [CryptoPriceTool()]
        system_prompt = """Tu es un expert en cryptomonnaies. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Prix et tendances des cryptomonnaies
- Analyse technique basique
- Actualités crypto

STYLE:
- Conversationnel et naturel
- Intègre les données de prix de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_crypto",
            name="Expert Crypto",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select crypto tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for crypto"""
        return None


class StockSubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in stock queries"""
    
    def __init__(self):
        tools = [StockQuoteTool(), MarketNewsTool()]
        system_prompt = """Tu es un expert en actions boursières. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Cotations d'actions
- Analyse de sociétés
- Tendances boursières

STYLE:
- Conversationnel et naturel
- Intègre les données de marché de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_stock",
            name="Expert Actions",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select stock tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for stock"""
        return None


class MarketSubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in market/indices queries"""
    
    def __init__(self):
        tools = [MarketSummaryTool(), MarketNewsTool()]
        system_prompt = """Tu es un expert en marchés financiers et indices boursiers. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Indices boursiers (S&P 500, NASDAQ, Dow Jones)
- Tendances de marché
- Analyse macroéconomique

STYLE:
- Conversationnel et naturel
- Intègre les données de marché de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_market",
            name="Expert Marchés",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select market tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for market"""
        return None


class CurrencySubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in currency exchange queries"""
    
    def __init__(self):
        tools = [CurrencyRateTool()]
        system_prompt = """Tu es un expert en devises et taux de change. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Taux de change
- Conversion de devises
- Tendances des devises

STYLE:
- Conversationnel et naturel
- Intègre les données de change de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_currency",
            name="Expert Devises",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select currency tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for currency"""
        return None


class FinanceAgent(ConversationalQualityAgent):
    """Main Finance Agent with sub-agents routing"""
    
    def __init__(self):
        # Create sub-agents
        sub_agents = [
            CryptoSubAgent(),
            StockSubAgent(),
            MarketSubAgent(),
            CurrencySubAgent()
        ]
        
        # All tools available to main agent
        tools = [
            CryptoPriceTool(),
            StockQuoteTool(),
            MarketSummaryTool(),
            CurrencyRateTool(),
            MarketNewsTool()
        ]
        
        system_prompt = """Tu es un expert financier. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Cryptomonnaies
- Actions boursières
- Marchés financiers
- Devises

STYLE:
- Conversationnel et naturel
- Intègre les données de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance",
            name="Expert Finance",
            system_prompt=system_prompt,
            tools=tools,
            sub_agents=sub_agents
        )
        
        self.query_detector = FinanceQueryDetector()
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select tools based on query type"""
        detection = self.query_detector.detect_query_type(query)
        query_type = detection.get("type", "general")
        
        selected_tools = []
        
        if query_type == "crypto":
            selected_tools = [tool for tool in self.tools if tool.name == "crypto_price"]
        elif query_type == "stock":
            selected_tools = [tool for tool in self.tools if tool.name in ["stock_quote", "market_news"]]
        elif query_type == "market":
            selected_tools = [tool for tool in self.tools if tool.name in ["market_summary", "market_news"]]
        elif query_type == "currency":
            selected_tools = [tool for tool in self.tools if tool.name == "currency_rate"]
        else:  # general
            # For general queries, try market summary and news
            selected_tools = [tool for tool in self.tools if tool.name in ["market_summary", "market_news"]]
        
        return selected_tools if selected_tools else [self.tools[0]]  # Fallback to first tool
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """Route to appropriate sub-agent based on query type"""
        detection = self.query_detector.detect_query_type(query)
        query_type = detection.get("type", "general")
        confidence = detection.get("confidence", 0.0)
        
        # Only route if confidence is high enough
        if confidence < 0.5:
            return None
        
        # Route to sub-agent
        for sub_agent in self.sub_agents:
            if sub_agent.agent_id == f"finance_{query_type}":
                return sub_agent
        
        return None


Finance Agent with sub-agents (Crypto, Stock, Market, Currency)
"""
import logging
from typing import List, Optional

from .base_agent import ConversationalQualityAgent
from .base_tool import BaseTool
from .tools.finance_tools import (
    CryptoPriceTool,
    StockQuoteTool,
    MarketSummaryTool,
    CurrencyRateTool,
    MarketNewsTool
)
from services.finance_query_detector import FinanceQueryDetector

logger = logging.getLogger(__name__)


class CryptoSubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in cryptocurrency queries"""
    
    def __init__(self):
        tools = [CryptoPriceTool()]
        system_prompt = """Tu es un expert en cryptomonnaies. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Prix et tendances des cryptomonnaies
- Analyse technique basique
- Actualités crypto

STYLE:
- Conversationnel et naturel
- Intègre les données de prix de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_crypto",
            name="Expert Crypto",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select crypto tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for crypto"""
        return None


class StockSubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in stock queries"""
    
    def __init__(self):
        tools = [StockQuoteTool(), MarketNewsTool()]
        system_prompt = """Tu es un expert en actions boursières. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Cotations d'actions
- Analyse de sociétés
- Tendances boursières

STYLE:
- Conversationnel et naturel
- Intègre les données de marché de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_stock",
            name="Expert Actions",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select stock tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for stock"""
        return None


class MarketSubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in market/indices queries"""
    
    def __init__(self):
        tools = [MarketSummaryTool(), MarketNewsTool()]
        system_prompt = """Tu es un expert en marchés financiers et indices boursiers. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Indices boursiers (S&P 500, NASDAQ, Dow Jones)
- Tendances de marché
- Analyse macroéconomique

STYLE:
- Conversationnel et naturel
- Intègre les données de marché de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_market",
            name="Expert Marchés",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select market tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for market"""
        return None


class CurrencySubAgent(ConversationalQualityAgent):
    """Sub-agent specialized in currency exchange queries"""
    
    def __init__(self):
        tools = [CurrencyRateTool()]
        system_prompt = """Tu es un expert en devises et taux de change. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Taux de change
- Conversion de devises
- Tendances des devises

STYLE:
- Conversationnel et naturel
- Intègre les données de change de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance_currency",
            name="Expert Devises",
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select currency tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for currency"""
        return None


class FinanceAgent(ConversationalQualityAgent):
    """Main Finance Agent with sub-agents routing"""
    
    def __init__(self):
        # Create sub-agents
        sub_agents = [
            CryptoSubAgent(),
            StockSubAgent(),
            MarketSubAgent(),
            CurrencySubAgent()
        ]
        
        # All tools available to main agent
        tools = [
            CryptoPriceTool(),
            StockQuoteTool(),
            MarketSummaryTool(),
            CurrencyRateTool(),
            MarketNewsTool()
        ]
        
        system_prompt = """Tu es un expert financier. Tu réponds dans la langue de l'utilisateur avec un ton conversationnel naturel.

EXPERTISE:
- Cryptomonnaies
- Actions boursières
- Marchés financiers
- Devises

STYLE:
- Conversationnel et naturel
- Intègre les données de manière fluide
- Évite les listes sauf si demandé explicitement
- Pose des questions de suivi si pertinent

{context}"""
        
        super().__init__(
            agent_id="finance",
            name="Expert Finance",
            system_prompt=system_prompt,
            tools=tools,
            sub_agents=sub_agents
        )
        
        self.query_detector = FinanceQueryDetector()
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """Select tools based on query type"""
        detection = self.query_detector.detect_query_type(query)
        query_type = detection.get("type", "general")
        
        selected_tools = []
        
        if query_type == "crypto":
            selected_tools = [tool for tool in self.tools if tool.name == "crypto_price"]
        elif query_type == "stock":
            selected_tools = [tool for tool in self.tools if tool.name in ["stock_quote", "market_news"]]
        elif query_type == "market":
            selected_tools = [tool for tool in self.tools if tool.name in ["market_summary", "market_news"]]
        elif query_type == "currency":
            selected_tools = [tool for tool in self.tools if tool.name == "currency_rate"]
        else:  # general
            # For general queries, try market summary and news
            selected_tools = [tool for tool in self.tools if tool.name in ["market_summary", "market_news"]]
        
        return selected_tools if selected_tools else [self.tools[0]]  # Fallback to first tool
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """Route to appropriate sub-agent based on query type"""
        detection = self.query_detector.detect_query_type(query)
        query_type = detection.get("type", "general")
        confidence = detection.get("confidence", 0.0)
        
        # Only route if confidence is high enough
        if confidence < 0.5:
            return None
        
        # Route to sub-agent
        for sub_agent in self.sub_agents:
            if sub_agent.agent_id == f"finance_{query_type}":
                return sub_agent
        
        return None



