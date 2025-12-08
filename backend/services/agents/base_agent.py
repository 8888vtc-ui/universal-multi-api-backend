"""
Base Agent class with Quality First strategy and Conversational format
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod

from services.ai_router import ai_router
from services.conversation_manager import ConversationManager
from services.context_helpers import detect_language, get_language_instruction
from .base_tool import BaseTool

logger = logging.getLogger(__name__)


class ConversationalQualityAgent(ABC):
    """
    Base agent class implementing Quality First strategy:
    1. Call data APIs first
    2. AI always responds (with or without data)
    3. Continuously re-query APIs to maximize information
    4. Format: conversational only (no blocks unless user requests)
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        system_prompt: str,
        tools: List[BaseTool],
        sub_agents: Optional[List['ConversationalQualityAgent']] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools
        self.sub_agents = sub_agents or []
        self.conversation_manager = ConversationManager()
    
    @abstractmethod
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """
        Select which tools to use based on the query
        Returns list of tools to execute
        """
        pass
    
    @abstractmethod
    def route_to_sub_agent(self, query: str) -> Optional['ConversationalQualityAgent']:  # type: ignore
        """
        Route query to appropriate sub-agent if needed
        Returns sub-agent or None
        """
        pass
    
    async def execute_tools(self, tools: List[BaseTool], query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute all tools in parallel and aggregate results
        """
        results = {
            "successful": [],
            "failed": [],
            "all_data": []
        }
        
        # Execute tools in parallel
        tasks = [tool.execute(query, **kwargs) for tool in tools]
        tool_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(tool_results):
            tool = tools[i]
            if isinstance(result, Exception):
                logger.warning(f"Tool {tool.name} failed: {result}")
                results["failed"].append({
                    "tool": tool.name,
                    "error": str(result)
                })
            elif result.get("success"):
                results["successful"].append({
                    "tool": tool.name,
                    "data": result.get("data"),
                    "source": result.get("source", tool.name)
                })
                results["all_data"].append(result.get("data"))
            else:
                results["failed"].append({
                    "tool": tool.name,
                    "error": result.get("error", "Unknown error")
                })
        
        return results
    
    async def enhance_with_ai(
        self,
        query: str,
        context_data: Dict[str, Any],
        language: str,
        conversation_history: Optional[str] = None,
        iteration: int = 1
    ) -> Dict[str, Any]:
        """
        Generate AI response with Quality First strategy:
        - Always respond (with or without data)
        - Enrich with data if available
        - Re-query if needed for quality
        """
        # Build context string
        context_parts = []
        if context_data.get("successful"):
            for item in context_data["successful"]:
                context_parts.append(f"[{item['source']}]: {item['data']}")
        
        context_str = "\n\n".join(context_parts) if context_parts else "Aucune donnée disponible."
        
        # Add conversation history
        if conversation_history:
            context_str = f"{conversation_history}\n\n{context_str}"
        
        # Build system prompt
        system_prompt = self.system_prompt.replace("{context}", context_str)
        
        # Add language instruction
        lang_instruction = get_language_instruction(language)
        system_prompt += f"\n\n{lang_instruction}"
        
        # Add conversational format instruction
        system_prompt += """
        
IMPORTANT - FORMAT DE RÉPONSE:
- Réponds UNIQUEMENT en format conversationnel naturel (comme une discussion avec un humain)
- Évite les listes, énumérations, blocs d'information
- Intègre les données de manière naturelle dans la conversation
- Utilise un ton chaleureux et engageant
- Pose des questions de suivi si pertinent
- Ne répète JAMAIS le message d'introduction ou de bienvenue
- Si l'utilisateur demande explicitement une liste ou un format structuré, alors tu peux utiliser ce format
"""
        
        # Add quality check instruction for iteration > 1
        if iteration > 1:
            system_prompt += f"""
            
QUALITÉ - ITÉRATION {iteration}:
- Analyse ta réponse précédente
- Identifie les informations manquantes ou incertaines
- Utilise les nouvelles données pour renforcer la qualité
- Vérifie la cohérence avec les données disponibles
"""
        
        # Call AI
        try:
            result = await ai_router.route(
                prompt=query,
                system_prompt=system_prompt
            )
            
            return {
                "response": result["response"],
                "source": result["source"],
                "confidence": 1.0,  # Will be validated
                "iteration": iteration
            }
        except Exception as e:
            logger.error(f"AI call failed: {e}", exc_info=True)
            # Fallback response
            return {
                "response": f"Je comprends ta question, mais je rencontre une difficulté technique. Peux-tu reformuler ?",
                "source": "fallback",
                "confidence": 0.5,
                "iteration": iteration
            }
    
    async def analyze_response_quality(
        self,
        response: str,
        query: str,
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze response quality and determine if re-query is needed
        Returns: {needs_requery: bool, missing_info: List[str], confidence: float}
        """
        # Simple quality checks
        missing_indicators = [
            "je ne sais pas",
            "je ne peux pas",
            "aucune donnée",
            "pas d'information",
            "données insuffisantes"
        ]
        
        has_missing = any(indicator in response.lower() for indicator in missing_indicators)
        
        # Check if we have data but didn't use it
        has_data = len(context_data.get("successful", [])) > 0
        uses_data = any(
            source.lower() in response.lower() 
            for source in [item["source"] for item in context_data.get("successful", [])]
        )
        
        # Determine if re-query needed
        needs_requery = False
        missing_info = []
        
        if has_missing and has_data and not uses_data:
            needs_requery = True
            missing_info.append("Données disponibles mais non utilisées")
        
        if has_missing and not has_data:
            needs_requery = True
            missing_info.append("Données manquantes")
        
        # Confidence score
        confidence = 0.9
        if has_missing:
            confidence -= 0.3
        if has_data and not uses_data:
            confidence -= 0.2
        
        return {
            "needs_requery": needs_requery,
            "missing_info": missing_info,
            "confidence": max(0.0, confidence)
        }
    
    async def chat(
        self,
        query: str,
        session_id: str,
        user_id: Optional[str] = None,
        language: Optional[str] = None,
        max_iterations: int = 2
    ) -> Dict[str, Any]:
        """
        Main chat method implementing Quality First strategy
        
        Flow:
        1. Route to sub-agent if needed
        2. Select and execute tools (data APIs)
        3. Generate AI response (always)
        4. Analyze quality
        5. Re-query if needed (max iterations)
        6. Return final response
        """
        # Auto-detect language
        detected_lang = detect_language(query)
        final_language = language or detected_lang
        
        # Check if should route to sub-agent
        sub_agent = self.route_to_sub_agent(query)
        if sub_agent:
            logger.info(f"Routing to sub-agent: {sub_agent.agent_id}")
            return await sub_agent.chat(query, session_id, user_id, final_language, max_iterations)
        
        # Get conversation history
        history = self.conversation_manager.get_conversation_history(
            session_id=session_id,
            expert_id=self.agent_id,
            limit=10
        )
        history_context = self.conversation_manager.format_history_for_prompt(history) if history else None
        
        # Select tools
        tools = self.select_tools(query)
        
        # Execute tools (data APIs) - FIRST
        context_data = await self.execute_tools(tools, query)
        
        # Generate AI response - ALWAYS (iteration 1)
        ai_response = await self.enhance_with_ai(
            query=query,
            context_data=context_data,
            language=final_language,
            conversation_history=history_context,
            iteration=1
        )
        
        # Analyze quality
        quality_analysis = await self.analyze_response_quality(
            response=ai_response["response"],
            query=query,
            context_data=context_data
        )
        
        # Re-query if needed (Quality First)
        final_response = ai_response["response"]
        iterations_used = 1
        
        if quality_analysis["needs_requery"] and max_iterations > 1:
            logger.info(f"Quality check: re-querying for better quality (missing: {quality_analysis['missing_info']})")
            
            # Re-execute tools to get more data
            context_data_requery = await self.execute_tools(tools, query)
            
            # Merge with previous data
            context_data["successful"].extend(context_data_requery.get("successful", []))
            context_data["all_data"].extend(context_data_requery.get("all_data", []))
            
            # Generate improved response (iteration 2)
            ai_response_improved = await self.enhance_with_ai(
                query=query,
                context_data=context_data,
                language=final_language,
                conversation_history=history_context,
                iteration=2
            )
            
            final_response = ai_response_improved["response"]
            iterations_used = 2
        
        # Save conversation
        self.conversation_manager.add_message(
            session_id=session_id,
            expert_id=self.agent_id,
            user_id=user_id,
            role="user",
            message=query
        )
        
        self.conversation_manager.add_message(
            session_id=session_id,
            expert_id=self.agent_id,
            user_id=user_id,
            role="assistant",
            message=final_response
        )
        
        return {
            "response": final_response,
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "sources": [item["source"] for item in context_data.get("successful", [])],
            "iterations": iterations_used,
            "confidence": quality_analysis["confidence"],
            "language": final_language
        }


"""
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from abc import ABC, abstractmethod

from services.ai_router import ai_router
from services.conversation_manager import ConversationManager
from services.context_helpers import detect_language, get_language_instruction
from .base_tool import BaseTool

logger = logging.getLogger(__name__)


class ConversationalQualityAgent(ABC):
    """
    Base agent class implementing Quality First strategy:
    1. Call data APIs first
    2. AI always responds (with or without data)
    3. Continuously re-query APIs to maximize information
    4. Format: conversational only (no blocks unless user requests)
    """
    
    def __init__(
        self,
        agent_id: str,
        name: str,
        system_prompt: str,
        tools: List[BaseTool],
        sub_agents: Optional[List['ConversationalQualityAgent']] = None
    ):
        self.agent_id = agent_id
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools
        self.sub_agents = sub_agents or []
        self.conversation_manager = ConversationManager()
    
    @abstractmethod
    def select_tools(self, query: str, detected_type: Optional[str] = None) -> List[BaseTool]:
        """
        Select which tools to use based on the query
        Returns list of tools to execute
        """
        pass
    
    @abstractmethod
    def route_to_sub_agent(self, query: str) -> Optional['ConversationalQualityAgent']:  # type: ignore
        """
        Route query to appropriate sub-agent if needed
        Returns sub-agent or None
        """
        pass
    
    async def execute_tools(self, tools: List[BaseTool], query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute all tools in parallel and aggregate results
        """
        results = {
            "successful": [],
            "failed": [],
            "all_data": []
        }
        
        # Execute tools in parallel
        tasks = [tool.execute(query, **kwargs) for tool in tools]
        tool_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(tool_results):
            tool = tools[i]
            if isinstance(result, Exception):
                logger.warning(f"Tool {tool.name} failed: {result}")
                results["failed"].append({
                    "tool": tool.name,
                    "error": str(result)
                })
            elif result.get("success"):
                results["successful"].append({
                    "tool": tool.name,
                    "data": result.get("data"),
                    "source": result.get("source", tool.name)
                })
                results["all_data"].append(result.get("data"))
            else:
                results["failed"].append({
                    "tool": tool.name,
                    "error": result.get("error", "Unknown error")
                })
        
        return results
    
    async def enhance_with_ai(
        self,
        query: str,
        context_data: Dict[str, Any],
        language: str,
        conversation_history: Optional[str] = None,
        iteration: int = 1
    ) -> Dict[str, Any]:
        """
        Generate AI response with Quality First strategy:
        - Always respond (with or without data)
        - Enrich with data if available
        - Re-query if needed for quality
        """
        # Build context string
        context_parts = []
        if context_data.get("successful"):
            for item in context_data["successful"]:
                context_parts.append(f"[{item['source']}]: {item['data']}")
        
        context_str = "\n\n".join(context_parts) if context_parts else "Aucune donnée disponible."
        
        # Add conversation history
        if conversation_history:
            context_str = f"{conversation_history}\n\n{context_str}"
        
        # Build system prompt
        system_prompt = self.system_prompt.replace("{context}", context_str)
        
        # Add language instruction
        lang_instruction = get_language_instruction(language)
        system_prompt += f"\n\n{lang_instruction}"
        
        # Add conversational format instruction
        system_prompt += """
        
IMPORTANT - FORMAT DE RÉPONSE:
- Réponds UNIQUEMENT en format conversationnel naturel (comme une discussion avec un humain)
- Évite les listes, énumérations, blocs d'information
- Intègre les données de manière naturelle dans la conversation
- Utilise un ton chaleureux et engageant
- Pose des questions de suivi si pertinent
- Ne répète JAMAIS le message d'introduction ou de bienvenue
- Si l'utilisateur demande explicitement une liste ou un format structuré, alors tu peux utiliser ce format
"""
        
        # Add quality check instruction for iteration > 1
        if iteration > 1:
            system_prompt += f"""
            
QUALITÉ - ITÉRATION {iteration}:
- Analyse ta réponse précédente
- Identifie les informations manquantes ou incertaines
- Utilise les nouvelles données pour renforcer la qualité
- Vérifie la cohérence avec les données disponibles
"""
        
        # Call AI
        try:
            result = await ai_router.route(
                prompt=query,
                system_prompt=system_prompt
            )
            
            return {
                "response": result["response"],
                "source": result["source"],
                "confidence": 1.0,  # Will be validated
                "iteration": iteration
            }
        except Exception as e:
            logger.error(f"AI call failed: {e}", exc_info=True)
            # Fallback response
            return {
                "response": f"Je comprends ta question, mais je rencontre une difficulté technique. Peux-tu reformuler ?",
                "source": "fallback",
                "confidence": 0.5,
                "iteration": iteration
            }
    
    async def analyze_response_quality(
        self,
        response: str,
        query: str,
        context_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze response quality and determine if re-query is needed
        Returns: {needs_requery: bool, missing_info: List[str], confidence: float}
        """
        # Simple quality checks
        missing_indicators = [
            "je ne sais pas",
            "je ne peux pas",
            "aucune donnée",
            "pas d'information",
            "données insuffisantes"
        ]
        
        has_missing = any(indicator in response.lower() for indicator in missing_indicators)
        
        # Check if we have data but didn't use it
        has_data = len(context_data.get("successful", [])) > 0
        uses_data = any(
            source.lower() in response.lower() 
            for source in [item["source"] for item in context_data.get("successful", [])]
        )
        
        # Determine if re-query needed
        needs_requery = False
        missing_info = []
        
        if has_missing and has_data and not uses_data:
            needs_requery = True
            missing_info.append("Données disponibles mais non utilisées")
        
        if has_missing and not has_data:
            needs_requery = True
            missing_info.append("Données manquantes")
        
        # Confidence score
        confidence = 0.9
        if has_missing:
            confidence -= 0.3
        if has_data and not uses_data:
            confidence -= 0.2
        
        return {
            "needs_requery": needs_requery,
            "missing_info": missing_info,
            "confidence": max(0.0, confidence)
        }
    
    async def chat(
        self,
        query: str,
        session_id: str,
        user_id: Optional[str] = None,
        language: Optional[str] = None,
        max_iterations: int = 2
    ) -> Dict[str, Any]:
        """
        Main chat method implementing Quality First strategy
        
        Flow:
        1. Route to sub-agent if needed
        2. Select and execute tools (data APIs)
        3. Generate AI response (always)
        4. Analyze quality
        5. Re-query if needed (max iterations)
        6. Return final response
        """
        # Auto-detect language
        detected_lang = detect_language(query)
        final_language = language or detected_lang
        
        # Check if should route to sub-agent
        sub_agent = self.route_to_sub_agent(query)
        if sub_agent:
            logger.info(f"Routing to sub-agent: {sub_agent.agent_id}")
            return await sub_agent.chat(query, session_id, user_id, final_language, max_iterations)
        
        # Get conversation history
        history = self.conversation_manager.get_conversation_history(
            session_id=session_id,
            expert_id=self.agent_id,
            limit=10
        )
        history_context = self.conversation_manager.format_history_for_prompt(history) if history else None
        
        # Select tools
        tools = self.select_tools(query)
        
        # Execute tools (data APIs) - FIRST
        context_data = await self.execute_tools(tools, query)
        
        # Generate AI response - ALWAYS (iteration 1)
        ai_response = await self.enhance_with_ai(
            query=query,
            context_data=context_data,
            language=final_language,
            conversation_history=history_context,
            iteration=1
        )
        
        # Analyze quality
        quality_analysis = await self.analyze_response_quality(
            response=ai_response["response"],
            query=query,
            context_data=context_data
        )
        
        # Re-query if needed (Quality First)
        final_response = ai_response["response"]
        iterations_used = 1
        
        if quality_analysis["needs_requery"] and max_iterations > 1:
            logger.info(f"Quality check: re-querying for better quality (missing: {quality_analysis['missing_info']})")
            
            # Re-execute tools to get more data
            context_data_requery = await self.execute_tools(tools, query)
            
            # Merge with previous data
            context_data["successful"].extend(context_data_requery.get("successful", []))
            context_data["all_data"].extend(context_data_requery.get("all_data", []))
            
            # Generate improved response (iteration 2)
            ai_response_improved = await self.enhance_with_ai(
                query=query,
                context_data=context_data,
                language=final_language,
                conversation_history=history_context,
                iteration=2
            )
            
            final_response = ai_response_improved["response"]
            iterations_used = 2
        
        # Save conversation
        self.conversation_manager.add_message(
            session_id=session_id,
            expert_id=self.agent_id,
            user_id=user_id,
            role="user",
            message=query
        )
        
        self.conversation_manager.add_message(
            session_id=session_id,
            expert_id=self.agent_id,
            user_id=user_id,
            role="assistant",
            message=final_response
        )
        
        return {
            "response": final_response,
            "agent_id": self.agent_id,
            "agent_name": self.name,
            "sources": [item["source"] for item in context_data.get("successful", [])],
            "iterations": iterations_used,
            "confidence": quality_analysis["confidence"],
            "language": final_language
        }

