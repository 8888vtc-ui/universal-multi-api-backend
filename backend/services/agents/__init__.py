"""
🤖 AGENT TEAM - The Autonomous AI Workforce - OPTIMIZED

All available agents for the orchestrator.
Each agent specializes in a specific domain.
"""
from .architect_agent import ArchitectAgent
from .developer_agent import DeveloperAgent
from .debugger_agent import DebuggerAgent
from .tester_agent import TesterAgent
from .monitor_agent import MonitorAgent
from .trading_agent import TradingAgent
from .documenter_agent import DocumenterAgent

# Agent registry for dynamic loading
AGENT_REGISTRY = {
    "architect": ArchitectAgent,
    "developer": DeveloperAgent,
    "debugger": DebuggerAgent,
    "tester": TesterAgent,
    "monitor": MonitorAgent,
    "trader": TradingAgent,
    "documenter": DocumenterAgent,
}

__all__ = [
    "ArchitectAgent",
    "DeveloperAgent", 
    "DebuggerAgent",
    "TesterAgent",
    "MonitorAgent",
    "TradingAgent",
    "DocumenterAgent",
    "AGENT_REGISTRY"
]
