"""
Base Tool class for agent tools
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Base class for all agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool
        
        Returns:
            Dict with keys:
                - success: bool
                - data: Any (the actual data)
                - error: Optional[str] (error message if failed)
                - source: str (API source name)
        """
        pass
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.name})>"


Base Tool class for agent tools
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class BaseTool(ABC):
    """Base class for all agent tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def execute(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the tool
        
        Returns:
            Dict with keys:
                - success: bool
                - data: Any (the actual data)
                - error: Optional[str] (error message if failed)
                - source: str (API source name)
        """
        pass
    
    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.name})>"



