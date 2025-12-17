"""
🤖 AGENT TEAM - The Autonomous AI Workforce - FULL EDITION

All available agents for the orchestrator.
11 specialized agents for complete automation.
"""
from .architect_agent import ArchitectAgent
from .developer_agent import DeveloperAgent
from .debugger_agent import DebuggerAgent
from .tester_agent import TesterAgent
from .monitor_agent import MonitorAgent
from .trading_agent import TradingAgent
from .documenter_agent import DocumenterAgent
from .security_agent import SecurityAgent
from .performance_agent import PerformanceAgent
from .devops_agent import DevOpsAgent
from .data_agent import DataAgent

# Agent registry for dynamic loading
AGENT_REGISTRY = {
    "architect": ArchitectAgent,
    "developer": DeveloperAgent,
    "debugger": DebuggerAgent,
    "tester": TesterAgent,
    "monitor": MonitorAgent,
    "trader": TradingAgent,
    "documenter": DocumenterAgent,
    "security": SecurityAgent,
    "performance": PerformanceAgent,
    "devops": DevOpsAgent,
    "data": DataAgent,
}

__all__ = [
    "ArchitectAgent",
    "DeveloperAgent", 
    "DebuggerAgent",
    "TesterAgent",
    "MonitorAgent",
    "TradingAgent",
    "DocumenterAgent",
    "SecurityAgent",
    "PerformanceAgent",
    "DevOpsAgent",
    "DataAgent",
    "AGENT_REGISTRY"
]
