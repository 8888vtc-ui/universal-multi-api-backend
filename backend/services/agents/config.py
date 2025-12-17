"""
🤖 AGENT DEFINITIONS - ULTIMATE EDITION (15 AGENTS)
Includes Meta Agent (creates agents) and Builder Agent (builds apps).
All free-tier AI models used as fallbacks.
"""

AGENTS = {
    "architect": {
        "name": "🏗️ Architect Agent",
        "model": "gpt-4o",
        "fallbacks": ["gpt-4o-mini", "groq", "gemini", "mistral", "deepseek", "cohere"],
        "role": "Analyse projets, specs, planning",
        "capabilities": ["analyze_codebase", "create_specs", "plan_tasks", "review_architecture", "estimate_effort"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "developer": {
        "name": "👨‍💻 Developer Agent", 
        "model": "claude-3.5-sonnet",
        "fallbacks": ["groq", "gemini", "mistral", "deepseek", "gpt-4o-mini", "cohere"],
        "role": "Code, features, refactoring",
        "capabilities": ["write_code", "implement_feature", "refactor", "fix_bugs", "code_review"],
        "priority": 2,
        "cost_tier": "premium"
    },
    "debugger": {
        "name": "🐛 Debugger Agent",
        "model": "deepseek-coder",
        "fallbacks": ["groq", "gemini", "mistral", "gpt-4o-mini", "cohere"],
        "role": "Debug, bugs, corrections",
        "capabilities": ["analyze_errors", "find_bugs", "suggest_fixes", "trace_issues", "root_cause_analysis"],
        "priority": 2,
        "cost_tier": "standard"
    },
    "tester": {
        "name": "🧪 Tester Agent",
        "model": "gpt-4o",
        "fallbacks": ["groq", "gemini", "mistral", "deepseek", "cohere"],
        "role": "Tests, QA, coverage",
        "capabilities": ["create_tests", "run_tests", "visual_testing", "qa_review", "coverage_analysis"],
        "priority": 3,
        "cost_tier": "premium"
    },
    "monitor": {
        "name": "📊 Monitor Agent",
        "model": "groq-llama3",
        "fallbacks": ["gemini", "mistral", "deepseek", "cohere"],
        "role": "Logs, anomalies, alertes",
        "capabilities": ["watch_logs", "detect_anomalies", "send_alerts", "report", "trend_analysis"],
        "priority": 1,
        "cost_tier": "free"
    },
    "trader": {
        "name": "📈 Trading Agent",
        "model": "gpt-4o",
        "fallbacks": ["groq", "gemini", "mistral", "perplexity", "cohere"],
        "role": "Trading, marchés, risques",
        "capabilities": ["market_analysis", "strategy_optimization", "position_monitoring", "risk_management", "backtest"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "documenter": {
        "name": "📚 Documenter Agent",
        "model": "groq-llama3",
        "fallbacks": ["gemini", "mistral", "deepseek", "cohere"],
        "role": "README, docs, guides",
        "capabilities": ["generate_readme", "api_docs", "user_guide", "changelog", "tutorials"],
        "priority": 4,
        "cost_tier": "free"
    },
    "security": {
        "name": "🔐 Security Agent",
        "model": "claude-3.5-sonnet",
        "fallbacks": ["groq", "gemini", "mistral", "deepseek", "gpt-4o-mini"],
        "role": "Audits, vulnérabilités, compliance",
        "capabilities": ["security_audit", "vulnerability_scan", "dependency_check", "compliance_check", "penetration_test", "secrets_scan"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "performance": {
        "name": "⚡ Performance Agent",
        "model": "groq-llama3",
        "fallbacks": ["gemini", "mistral", "deepseek", "cohere"],
        "role": "Bottlenecks, optimisation",
        "capabilities": ["analyze_performance", "find_bottlenecks", "optimize_code", "benchmark", "memory_analysis", "database_optimization"],
        "priority": 2,
        "cost_tier": "free"
    },
    "devops": {
        "name": "🔧 DevOps Agent",
        "model": "groq-llama3",
        "fallbacks": ["gemini", "mistral", "deepseek", "cohere"],
        "role": "CI/CD, deploy, infrastructure",
        "capabilities": ["deploy", "rollback", "create_pipeline", "infrastructure_review", "docker_optimize", "kubernetes_config", "monitoring_setup", "cost_optimization"],
        "priority": 2,
        "cost_tier": "free"
    },
    "data": {
        "name": "📊 Data Agent",
        "model": "gpt-4o",
        "fallbacks": ["groq", "gemini", "mistral", "deepseek", "cohere"],
        "role": "ML, analytics, prédictions",
        "capabilities": ["analyze_data", "create_model", "feature_engineering", "exploratory_analysis", "predict", "generate_report", "clean_data", "visualize"],
        "priority": 2,
        "cost_tier": "premium"
    },
    "notification": {
        "name": "📢 Notification Agent",
        "model": "groq-llama3",
        "fallbacks": ["gemini", "mistral", "cohere"],
        "role": "Alertes Telegram/Slack/Discord",
        "capabilities": ["send_alert", "send_telegram", "send_slack", "send_discord", "send_all", "format_message"],
        "priority": 1,
        "cost_tier": "free"
    },
    "api": {
        "name": "🌐 API Agent",
        "model": "groq-llama3",
        "fallbacks": ["gemini", "mistral", "deepseek", "cohere"],
        "role": "Tests API, endpoints, intégrations",
        "capabilities": ["test_endpoint", "test_endpoints", "validate_response", "load_test", "health_check", "generate_tests"],
        "priority": 2,
        "cost_tier": "free"
    },
    "meta": {
        "name": "🧬 Meta Agent",
        "model": "gpt-4o",
        "fallbacks": ["claude-3.5-sonnet", "groq", "gemini"],
        "role": "Crée et optimise les autres agents",
        "capabilities": ["create_agent", "modify_agent", "optimize_agent", "analyze_agents", "suggest_agents", "create_workflow", "generate_agent_code", "plan_agent_system"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "builder": {
        "name": "🏭 Builder Agent",
        "model": "gpt-4o",
        "fallbacks": ["claude-3.5-sonnet", "groq", "gemini"],
        "role": "Pipeline de construction automatique d'applications",
        "capabilities": ["start_build", "execute_phase", "get_build_status", "generate_plan", "create_project_structure", "full_build", "resume_build", "validate_phase"],
        "priority": 1,
        "cost_tier": "premium"
    }
}

# 20 Comprehensive workflows
WORKFLOWS = {
    # === APPLICATION BUILD WORKFLOWS ===
    "build_application": {
        "description": "Construction automatique complète d'une application (9 phases)",
        "parallel": False,
        "slow_but_thorough": True,
        "steps": [
            {"agent": "builder", "action": "generate_plan"},
            {"agent": "builder", "action": "execute_phase", "phase": "planning"},
            {"agent": "builder", "action": "execute_phase", "phase": "architecture"},
            {"agent": "builder", "action": "execute_phase", "phase": "security_review"},
            {"agent": "builder", "action": "execute_phase", "phase": "development"},
            {"agent": "builder", "action": "execute_phase", "phase": "testing"},
            {"agent": "builder", "action": "execute_phase", "phase": "documentation"},
            {"agent": "builder", "action": "execute_phase", "phase": "performance"},
            {"agent": "builder", "action": "execute_phase", "phase": "deployment"},
            {"agent": "builder", "action": "execute_phase", "phase": "monitoring"},
            {"agent": "notification", "action": "send_alert"}
        ]
    },
    "quick_prototype": {
        "description": "Prototype rapide (3 phases essentielles)",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "create_specs"},
            {"agent": "developer", "action": "implement_feature"},
            {"agent": "documenter", "action": "generate_readme"}
        ]
    },
    "create_new_agent": {
        "description": "Créer un nouvel agent personnalisé",
        "parallel": False,
        "steps": [
            {"agent": "meta", "action": "suggest_agents"},
            {"agent": "meta", "action": "create_agent"},
            {"agent": "meta", "action": "generate_agent_code"},
            {"agent": "tester", "action": "create_tests"}
        ]
    },
    
    # === STANDARD WORKFLOWS ===
    "fix_bug": {
        "description": "Corriger un bug détecté",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "detect_anomaly"},
            {"agent": "debugger", "action": "analyze_error"},
            {"agent": "developer", "action": "fix_bug"},
            {"agent": "tester", "action": "verify_fix"},
            {"agent": "devops", "action": "deploy"},
            {"agent": "notification", "action": "send_alert"}
        ]
    },
    "new_feature": {
        "description": "Nouvelle feature complète",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "create_specs"},
            {"agent": "developer", "action": "implement_feature"},
            {"agent": "security", "action": "security_audit"},
            {"agent": "tester", "action": "create_tests"},
            {"agent": "documenter", "action": "generate_docs"},
            {"agent": "devops", "action": "deploy"},
            {"agent": "notification", "action": "send_alert"}
        ]
    },
    "optimize_trading": {
        "description": "Optimiser bots trading",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "collect_metrics"},
            {"agent": "trader", "action": "analyze_performance"},
            {"agent": "data", "action": "analyze_data"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "performance", "action": "benchmark"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "daily_maintenance": {
        "description": "Maintenance quotidienne",
        "parallel": True,
        "steps": [
            {"agent": "monitor", "action": "health_check"},
            {"agent": "security", "action": "dependency_check"},
            {"agent": "performance", "action": "analyze_performance"},
            {"agent": "api", "action": "health_check"}
        ]
    },
    "full_security_audit": {
        "description": "Audit sécurité complet",
        "parallel": False,
        "steps": [
            {"agent": "security", "action": "security_audit"},
            {"agent": "security", "action": "vulnerability_scan"},
            {"agent": "security", "action": "dependency_check"},
            {"agent": "security", "action": "secrets_scan"},
            {"agent": "documenter", "action": "generate_report"},
            {"agent": "notification", "action": "send_alert"}
        ]
    },
    "performance_optimization": {
        "description": "Optimiser performances",
        "parallel": False,
        "steps": [
            {"agent": "performance", "action": "analyze_performance"},
            {"agent": "performance", "action": "find_bottlenecks"},
            {"agent": "performance", "action": "database_optimization"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "performance", "action": "benchmark"}
        ]
    },
    "analyze_project": {
        "description": "Analyser projet complet",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "analyze_codebase"},
            {"agent": "security", "action": "security_audit"},
            {"agent": "performance", "action": "analyze_performance"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "data_pipeline": {
        "description": "Pipeline ML/Data",
        "parallel": False,
        "steps": [
            {"agent": "data", "action": "exploratory_analysis"},
            {"agent": "data", "action": "clean_data"},
            {"agent": "data", "action": "feature_engineering"},
            {"agent": "data", "action": "create_model"},
            {"agent": "data", "action": "generate_report"}
        ]
    },
    "full_deploy": {
        "description": "Déploiement complet",
        "parallel": False,
        "steps": [
            {"agent": "tester", "action": "run_tests"},
            {"agent": "security", "action": "security_audit"},
            {"agent": "performance", "action": "benchmark"},
            {"agent": "devops", "action": "deploy"},
            {"agent": "api", "action": "health_check"},
            {"agent": "notification", "action": "send_alert"}
        ]
    },
    "generate_documentation": {
        "description": "Documentation complète",
        "parallel": True,
        "steps": [
            {"agent": "documenter", "action": "generate_readme"},
            {"agent": "documenter", "action": "api_docs"},
            {"agent": "documenter", "action": "user_guide"}
        ]
    },
    "infrastructure_review": {
        "description": "Review infrastructure",
        "parallel": True,
        "steps": [
            {"agent": "devops", "action": "infrastructure_review"},
            {"agent": "devops", "action": "cost_optimization"},
            {"agent": "security", "action": "compliance_check"},
            {"agent": "performance", "action": "analyze_performance"}
        ]
    },
    "api_testing": {
        "description": "Tests API complets",
        "parallel": False,
        "steps": [
            {"agent": "api", "action": "test_endpoints"},
            {"agent": "api", "action": "load_test"},
            {"agent": "api", "action": "generate_tests"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "quick_fix": {
        "description": "Fix rapide",
        "parallel": False,
        "steps": [
            {"agent": "debugger", "action": "analyze_error"},
            {"agent": "developer", "action": "fix_bug"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "ml_project": {
        "description": "Projet ML complet",
        "parallel": False,
        "steps": [
            {"agent": "data", "action": "exploratory_analysis"},
            {"agent": "data", "action": "feature_engineering"},
            {"agent": "data", "action": "create_model"},
            {"agent": "performance", "action": "benchmark"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "auto_improve": {
        "description": "Amélioration continue",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "analyze_trends"},
            {"agent": "performance", "action": "find_bottlenecks"},
            {"agent": "architect", "action": "propose_improvements"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "tester", "action": "run_tests"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "plan_agent_ecosystem": {
        "description": "Planifier un écosystème d'agents",
        "parallel": False,
        "steps": [
            {"agent": "meta", "action": "analyze_agents"},
            {"agent": "meta", "action": "suggest_agents"},
            {"agent": "meta", "action": "plan_agent_system"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "alert_system_test": {
        "description": "Tester système alertes",
        "parallel": False,
        "steps": [
            {"agent": "notification", "action": "check_status"},
            {"agent": "notification", "action": "send_all"}
        ]
    }
}

# 22 Quick actions
QUICK_ACTIONS = {
    # Standard actions
    "analyze_code": {"agent": "architect", "action": "analyze_codebase"},
    "review_pr": {"agent": "developer", "action": "code_review"},
    "find_bugs": {"agent": "debugger", "action": "find_bugs"},
    "write_tests": {"agent": "tester", "action": "create_tests"},
    "deploy": {"agent": "devops", "action": "deploy"},
    "check_health": {"agent": "monitor", "action": "health_check"},
    "analyze_market": {"agent": "trader", "action": "market_analysis"},
    "generate_docs": {"agent": "documenter", "action": "generate_readme"},
    "security_scan": {"agent": "security", "action": "vulnerability_scan"},
    "find_bottlenecks": {"agent": "performance", "action": "find_bottlenecks"},
    "create_pipeline": {"agent": "devops", "action": "create_pipeline"},
    "analyze_data": {"agent": "data", "action": "analyze_data"},
    "create_model": {"agent": "data", "action": "create_model"},
    "cost_optimize": {"agent": "devops", "action": "cost_optimization"},
    "send_alert": {"agent": "notification", "action": "send_alert"},
    "test_api": {"agent": "api", "action": "test_endpoint"},
    "load_test": {"agent": "api", "action": "load_test"},
    
    # Meta & Builder actions
    "create_agent": {"agent": "meta", "action": "create_agent"},
    "suggest_agents": {"agent": "meta", "action": "suggest_agents"},
    "start_build": {"agent": "builder", "action": "generate_plan"},
    "build_status": {"agent": "builder", "action": "get_build_status"},
    "full_build": {"agent": "builder", "action": "full_build"},
}

# Scheduled tasks
SCHEDULED_TASKS = {
    "morning_health_check": {
        "cron": "0 8 * * *",
        "workflow": "daily_maintenance"
    },
    "nightly_security_scan": {
        "cron": "0 2 * * *",
        "workflow": "full_security_audit"
    },
    "weekly_performance_review": {
        "cron": "0 10 * * 1",
        "workflow": "performance_optimization"
    },
    "trading_optimization": {
        "cron": "0 */4 * * *",
        "action": {"agent": "trader", "action": "analyze_performance"}
    },
    "hourly_monitoring": {
        "cron": "0 * * * *",
        "action": {"agent": "monitor", "action": "health_check"}
    },
    "api_health_check": {
        "cron": "*/30 * * * *",
        "action": {"agent": "api", "action": "health_check"}
    },
    "weekly_agent_analysis": {
        "cron": "0 9 * * 0",
        "action": {"agent": "meta", "action": "analyze_agents"}
    }
}

# Build phases for the Builder Agent
BUILD_PHASES = [
    "planning",
    "architecture", 
    "security_review",
    "development",
    "testing",
    "documentation",
    "performance",
    "deployment",
    "monitoring"
]
