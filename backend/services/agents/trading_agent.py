"""
💰 TRADING AGENT
Uses GPT-4o for market analysis and strategy optimization.
"""
from typing import Dict, Any
from .base_agent import BaseAgent


class TradingAgent(BaseAgent):
    """Analyzes markets, optimizes trading strategies"""
    
    def __init__(self):
        super().__init__(
            name="💰 Trading Agent",
            model="gpt-4o",
            role="Analyse les marchés, optimise les stratégies trading, surveille les positions"
        )
    
    async def _do_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        action = task.get("action", "market_analysis")
        
        if action == "market_analysis":
            return await self._market_analysis(task)
        elif action == "strategy_optimization":
            return await self._strategy_optimization(task)
        elif action == "position_monitoring":
            return await self._position_monitoring(task)
        elif action == "risk_management":
            return await self._risk_management(task)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}
    
    async def _market_analysis(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze market conditions"""
        symbol = task.get("symbol", "BTC")
        data = task.get("market_data", {})
        
        prompt = f"""
        Analyse le marché pour {symbol}:
        
        Données: {data}
        
        Fournis:
        1. Tendance actuelle (bullish/bearish/neutral)
        2. Niveaux clés (support/resistance)
        3. Indicateurs techniques
        4. Sentiment du marché
        5. Signal recommandé (BUY/SELL/HOLD)
        6. Niveau de confiance (1-10)
        
        Format: JSON structuré
        """
        result = await self.think(prompt)
        return {"success": True, "analysis": result}
    
    async def _strategy_optimization(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize trading strategy parameters"""
        current_strategy = task.get("strategy", {})
        performance = task.get("performance", {})
        
        prompt = f"""
        Optimise cette stratégie de trading:
        
        Stratégie actuelle: {current_strategy}
        Performance récente: {performance}
        
        Propose des ajustements pour:
        1. Stop-loss (%)
        2. Take-profit (%)
        3. Taille de position
        4. Critères d'entrée
        5. Critères de sortie
        
        Justifie chaque recommandation.
        Format: JSON avec paramètres et justifications
        """
        result = await self.think(prompt)
        return {"success": True, "optimizations": result}
    
    async def _position_monitoring(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Monitor open positions"""
        positions = task.get("positions", [])
        
        prompt = f"""
        Analyse ces positions ouvertes:
        
        Positions: {positions}
        
        Pour chaque position:
        1. Risque actuel
        2. P&L non réalisé
        3. Action recommandée (keep/close/adjust)
        4. Raison
        
        Alerte si risque > 5% du portfolio
        """
        result = await self.think(prompt)
        return {"success": True, "monitoring": result}
    
    async def _risk_management(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Assess and manage portfolio risk"""
        portfolio = task.get("portfolio", {})
        
        prompt = f"""
        Évalue le risque de ce portfolio:
        
        Portfolio: {portfolio}
        
        Analyse:
        1. Exposition totale
        2. Corrélations entre actifs
        3. VaR (Value at Risk) estimé
        4. Diversification
        5. Recommandations pour réduire le risque
        
        Format: Rapport de risque complet
        """
        result = await self.think(prompt)
        return {"success": True, "risk_report": result}
