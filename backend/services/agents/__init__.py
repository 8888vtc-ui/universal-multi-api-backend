"""
🤖 AGENT TEAM - The Autonomous AI Workforce - ULTIMATE EDITION

15 specialized agents for complete automation.
Includes Meta Agent (creates agents) and Builder Agent (builds apps).
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
from .notification_agent import NotificationAgent
from .api_agent import ApiAgent
from .meta_agent import MetaAgent
from .builder_agent import BuilderAgent

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
    "notification": NotificationAgent,
    "api": ApiAgent,
    "meta": MetaAgent,
    "builder": BuilderAgent,
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
    "NotificationAgent",
    "ApiAgent",
    "MetaAgent",
    "BuilderAgent",
    "AGENT_REGISTRY"
]
