"""
Agent Factory - Creates all agents from expert configuration
"""
import logging
from typing import Dict, Optional

from .base_agent import ConversationalQualityAgent
from .base_tool import BaseTool
from .finance_agent import FinanceAgent
from services.expert_config import ExpertId, get_expert

logger = logging.getLogger(__name__)


class SimpleDataTool(BaseTool):
    """Simple tool that calls a data API endpoint"""
    
    def __init__(self, name: str, description: str, endpoint: str):
        super().__init__(name, description)
        self.endpoint = endpoint
        import os
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict:
        """Execute API call"""
        import httpx
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Build URL with query
                url = f"{self.base_url}{self.endpoint}"
                if "{query}" in self.endpoint:
                    url = url.replace("{query}", query)
                elif "?" in url:
                    url = f"{url}&q={query}"
                else:
                    url = f"{url}?q={query}"
                
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "data": str(data),
                        "source": self.name
                    }
                
                return {
                    "success": False,
                    "error": f"Status {response.status_code}",
                    "source": self.name
                }
        except Exception as e:
            logger.error(f"SimpleDataTool {self.name} error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": self.name
            }


class GenericAgent(ConversationalQualityAgent):
    """Generic agent for non-finance experts"""
    
    def __init__(self, expert_id: str, expert_config):
        # Create tools from data_apis - COMPLETE mapping
        tools = []
        api_endpoints = {
            # Basic APIs
            "wikipedia": "/wikipedia/search?q={query}&limit=2",
            "weather": "/weather/current?location={query}",
            "countries": "/countries/search?q={query}",
            "sports": "/sports/news?q={query}",
            "news": "/news/search?q={query}&limit=3",
            "jokes": "/jokes/random",
            "quotes": "/quotes/random",
            # Health & Nutrition
            "nutrition": "/nutrition/search?q={query}",
            "medical": "/medical/research/search?q={query}",
            "medical_research": "/medical/research/search?q={query}",
            "medical_drugs": "/medical/drugs/search?q={query}",
            # Content
            "books": "/books/search?q={query}&limit=2",
            "trivia": "/trivia/random",
            "geocoding": "/geocoding/search?q={query}",
            "omdb": "/omdb/search?query={query}",
            "github": "/github/search/repos?q={query}",
            # Finance (basic - Finance agent handles specialized ones)
            "exchange": "/exchange/rates",
            "coincap": "/coincap/assets?search={query}",
            # Misc
            "numbers": "/numbers/random",
            "animals": "/animals/random",
            "history": "/history/today",
            "nameanalysis": "/nameanalysis/analyze?name={query}",
            # Finance specialized (will be handled by Finance agent, but include for fallback)
            "finance_stock": "/finance/stock/quote/{query}",
            "finance_company": "/finance/stock/company/{query}",
            "finance_news": "/finance/stock/news/{query}?limit=5",
            "finance_market_news": "/finance/market/news?limit=5",
        }
        
        for api_name in expert_config.data_apis:
            if api_name in api_endpoints:
                endpoint = api_endpoints[api_name]
                # Endpoint will be processed by SimpleDataTool.execute() with {query} replacement
                
                tools.append(SimpleDataTool(
                    name=api_name,
                    description=f"Fetch data from {api_name}",
                    endpoint=endpoint
                ))
        
        # If no tools, add a generic one
        if not tools:
            tools.append(SimpleDataTool(
                name="generic",
                description="Generic data source",
                endpoint="/news/search?q={query}&limit=3"
            ))
        
        # Get system prompt from config
        system_prompt = expert_config.system_prompt
        
        super().__init__(
            agent_id=expert_id,
            name=expert_config.name,
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> list:
        """Select all available tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for generic agents"""
        return None


class AgentFactory:
    """Factory to create all agents"""
    
    _agents: Dict[str, ConversationalQualityAgent] = {}
    
    @classmethod
    def get_agent(cls, expert_id: str) -> Optional[ConversationalQualityAgent]:
        """Get agent by expert ID"""
        if expert_id not in cls._agents:
            cls._agents[expert_id] = cls._create_agent(expert_id)
        
        return cls._agents.get(expert_id)
    
    @classmethod
    def _create_agent(cls, expert_id: str) -> Optional[ConversationalQualityAgent]:
        """Create agent from expert ID"""
        try:
            expert_config = get_expert(ExpertId(expert_id))
            
            # Special handling for Finance
            if expert_id == "finance":
                return FinanceAgent()
            
            # Generic agents for others
            return GenericAgent(expert_id, expert_config)
        
        except Exception as e:
            logger.error(f"Failed to create agent {expert_id}: {e}", exc_info=True)
            return None
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, ConversationalQualityAgent]:
        """Get all available agents"""
        # Initialize all agents
        for expert_id in ExpertId:
            if expert_id.value not in cls._agents:
                cls._agents[expert_id.value] = cls._create_agent(expert_id.value)
        
        return cls._agents


"""
import logging
from typing import Dict, Optional

from .base_agent import ConversationalQualityAgent
from .base_tool import BaseTool
from .finance_agent import FinanceAgent
from services.expert_config import ExpertId, get_expert

logger = logging.getLogger(__name__)


class SimpleDataTool(BaseTool):
    """Simple tool that calls a data API endpoint"""
    
    def __init__(self, name: str, description: str, endpoint: str):
        super().__init__(name, description)
        self.endpoint = endpoint
        import os
        self.base_url = os.getenv("APP_URL", "http://localhost:8000") + "/api"
    
    async def execute(self, query: str, **kwargs) -> Dict:
        """Execute API call"""
        import httpx
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Build URL with query
                url = f"{self.base_url}{self.endpoint}"
                if "{query}" in self.endpoint:
                    url = url.replace("{query}", query)
                elif "?" in url:
                    url = f"{url}&q={query}"
                else:
                    url = f"{url}?q={query}"
                
                response = await client.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "success": True,
                        "data": str(data),
                        "source": self.name
                    }
                
                return {
                    "success": False,
                    "error": f"Status {response.status_code}",
                    "source": self.name
                }
        except Exception as e:
            logger.error(f"SimpleDataTool {self.name} error: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "source": self.name
            }


class GenericAgent(ConversationalQualityAgent):
    """Generic agent for non-finance experts"""
    
    def __init__(self, expert_id: str, expert_config):
        # Create tools from data_apis - COMPLETE mapping
        tools = []
        api_endpoints = {
            # Basic APIs
            "wikipedia": "/wikipedia/search?q={query}&limit=2",
            "weather": "/weather/current?location={query}",
            "countries": "/countries/search?q={query}",
            "sports": "/sports/news?q={query}",
            "news": "/news/search?q={query}&limit=3",
            "jokes": "/jokes/random",
            "quotes": "/quotes/random",
            # Health & Nutrition
            "nutrition": "/nutrition/search?q={query}",
            "medical": "/medical/search?q={query}",
            # Content
            "books": "/books/search?q={query}&limit=2",
            "trivia": "/trivia/random",
            "geocoding": "/geocoding/search?q={query}",
            "omdb": "/omdb/search?query={query}",
            "github": "/github/search/repos?q={query}",
            # Finance (basic - Finance agent handles specialized ones)
            "exchange": "/exchange/rates",
            "coincap": "/coincap/assets?search={query}",
            # Misc
            "numbers": "/numbers/random",
            "animals": "/animals/random",
            "history": "/history/today",
            "nameanalysis": "/nameanalysis/analyze?name={query}",
            # Finance specialized (will be handled by Finance agent, but include for fallback)
            "finance_stock": "/finance/stock/quote/{query}",
            "finance_company": "/finance/stock/company/{query}",
            "finance_news": "/finance/stock/news/{query}?limit=5",
            "finance_market_news": "/finance/market/news?limit=5",
        }
        
        for api_name in expert_config.data_apis:
            if api_name in api_endpoints:
                endpoint = api_endpoints[api_name]
                # Endpoint will be processed by SimpleDataTool.execute() with {query} replacement
                
                tools.append(SimpleDataTool(
                    name=api_name,
                    description=f"Fetch data from {api_name}",
                    endpoint=endpoint
                ))
        
        # If no tools, add a generic one
        if not tools:
            tools.append(SimpleDataTool(
                name="generic",
                description="Generic data source",
                endpoint="/news/search?q={query}&limit=3"
            ))
        
        # Get system prompt from config
        system_prompt = expert_config.system_prompt
        
        super().__init__(
            agent_id=expert_id,
            name=expert_config.name,
            system_prompt=system_prompt,
            tools=tools
        )
    
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> list:
        """Select all available tools"""
        return self.tools
    
    def route_to_sub_agent(self, query: str) -> Optional[ConversationalQualityAgent]:
        """No sub-agents for generic agents"""
        return None


class AgentFactory:
    """Factory to create all agents"""
    
    _agents: Dict[str, ConversationalQualityAgent] = {}
    
    @classmethod
    def get_agent(cls, expert_id: str) -> Optional[ConversationalQualityAgent]:
        """Get agent by expert ID"""
        if expert_id not in cls._agents:
            cls._agents[expert_id] = cls._create_agent(expert_id)
        
        return cls._agents.get(expert_id)
    
    @classmethod
    def _create_agent(cls, expert_id: str) -> Optional[ConversationalQualityAgent]:
        """Create agent from expert ID"""
        try:
            expert_config = get_expert(ExpertId(expert_id))
            
            # Special handling for Finance
            if expert_id == "finance":
                return FinanceAgent()
            
            # Generic agents for others
            return GenericAgent(expert_id, expert_config)
        
        except Exception as e:
            logger.error(f"Failed to create agent {expert_id}: {e}", exc_info=True)
            return None
    
    @classmethod
    def get_all_agents(cls) -> Dict[str, ConversationalQualityAgent]:
        """Get all available agents"""
        # Initialize all agents
        for expert_id in ExpertId:
            if expert_id.value not in cls._agents:
                cls._agents[expert_id.value] = cls._create_agent(expert_id.value)
        
        return cls._agents

