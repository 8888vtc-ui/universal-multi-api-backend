"""
🤖 AGENT DEFINITIONS - FULL EDITION (11 AGENTS)
Each agent has a specific role and uses the best AI model for that task.
"""

AGENTS = {
    "architect": {
        "name": "🏗️ Architect Agent",
        "model": "gpt-4o",
        "fallbacks": ["groq-llama3", "deepseek-coder"],
        "role": "Analyse les projets, crée les specs, planifie les tâches",
        "capabilities": ["analyze_codebase", "create_specs", "plan_tasks", "review_architecture", "estimate_effort"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "developer": {
        "name": "👨‍💻 Developer Agent", 
        "model": "claude-3.5-sonnet",
        "fallbacks": ["gpt-4o", "deepseek-coder"],
        "role": "Écrit le code, implémente les features, refactore",
        "capabilities": ["write_code", "implement_feature", "refactor", "fix_bugs", "code_review"],
        "priority": 2,
        "cost_tier": "premium"
    },
    "debugger": {
        "name": "🐛 Debugger Agent",
        "model": "deepseek-coder",
        "fallbacks": ["groq-llama3", "gpt-4o-mini"],
        "role": "Analyse les erreurs, trouve les bugs, propose des corrections",
        "capabilities": ["analyze_errors", "find_bugs", "suggest_fixes", "trace_issues", "root_cause_analysis"],
        "priority": 2,
        "cost_tier": "standard"
    },
    "tester": {
        "name": "🧪 Tester Agent",
        "model": "gpt-4o",
        "fallbacks": ["claude-3.5-sonnet", "groq-llama3"],
        "role": "Crée et exécute les tests, vérifie la qualité",
        "capabilities": ["create_tests", "run_tests", "visual_testing", "qa_review", "coverage_analysis"],
        "priority": 3,
        "cost_tier": "premium"
    },
    "monitor": {
        "name": "📊 Monitor Agent",
        "model": "groq-llama3",
        "fallbacks": ["gpt-4o-mini", "deepseek-coder"],
        "role": "Surveille les logs, détecte les anomalies, alerte",
        "capabilities": ["watch_logs", "detect_anomalies", "send_alerts", "report", "trend_analysis"],
        "priority": 1,
        "cost_tier": "standard"
    },
    "trader": {
        "name": "📈 Trading Agent",
        "model": "gpt-4o",
        "fallbacks": ["claude-3.5-sonnet", "groq-llama3"],
        "role": "Analyse les marchés, optimise les stratégies trading",
        "capabilities": ["market_analysis", "strategy_optimization", "position_monitoring", "risk_management", "backtest"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "documenter": {
        "name": "📚 Documenter Agent",
        "model": "groq-llama3",
        "fallbacks": ["gpt-4o-mini", "claude-3.5-sonnet"],
        "role": "Génère documentation, README, guides",
        "capabilities": ["generate_readme", "api_docs", "user_guide", "changelog", "tutorials"],
        "priority": 4,
        "cost_tier": "standard"
    },
    "security": {
        "name": "🔐 Security Agent",
        "model": "claude-3.5-sonnet",
        "fallbacks": ["gpt-4o", "deepseek-coder"],
        "role": "Audits sécurité, détection vulnérabilités, compliance",
        "capabilities": ["security_audit", "vulnerability_scan", "dependency_check", "compliance_check", "penetration_test", "secrets_scan"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "performance": {
        "name": "⚡ Performance Agent",
        "model": "groq-llama3",
        "fallbacks": ["deepseek-coder", "gpt-4o-mini"],
        "role": "Analyse performances, trouve bottlenecks, optimise",
        "capabilities": ["analyze_performance", "find_bottlenecks", "optimize_code", "benchmark", "memory_analysis", "database_optimization"],
        "priority": 2,
        "cost_tier": "standard"
    },
    "devops": {
        "name": "🔧 DevOps Agent",
        "model": "groq-llama3",
        "fallbacks": ["gpt-4o-mini", "deepseek-coder"],
        "role": "Déploiements, CI/CD, infrastructure, cloud",
        "capabilities": ["deploy", "rollback", "create_pipeline", "infrastructure_review", "docker_optimize", "kubernetes_config", "monitoring_setup", "cost_optimization"],
        "priority": 2,
        "cost_tier": "standard"
    },
    "data": {
        "name": "📊 Data Agent",
        "model": "gpt-4o",
        "fallbacks": ["claude-3.5-sonnet", "groq-llama3"],
        "role": "Analyse données, ML, feature engineering, prédictions",
        "capabilities": ["analyze_data", "create_model", "feature_engineering", "exploratory_analysis", "predict", "generate_report", "clean_data", "visualize"],
        "priority": 2,
        "cost_tier": "premium"
    }
}

# Comprehensive workflow definitions
WORKFLOWS = {
    "fix_bug": {
        "description": "Corriger un bug détecté",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "detect_anomaly"},
            {"agent": "debugger", "action": "analyze_error"},
            {"agent": "developer", "action": "fix_bug"},
            {"agent": "tester", "action": "verify_fix"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "new_feature": {
        "description": "Implémenter une nouvelle feature",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "create_specs"},
            {"agent": "developer", "action": "implement_feature"},
            {"agent": "security", "action": "security_audit"},
            {"agent": "tester", "action": "create_tests"},
            {"agent": "documenter", "action": "generate_docs"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "optimize_trading": {
        "description": "Optimiser les bots de trading",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "collect_metrics"},
            {"agent": "trader", "action": "analyze_performance"},
            {"agent": "data", "action": "analyze_data"},
            {"agent": "architect", "action": "propose_improvements"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "performance", "action": "benchmark"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "daily_maintenance": {
        "description": "Maintenance quotidienne automatique",
        "parallel": True,
        "steps": [
            {"agent": "monitor", "action": "health_check"},
            {"agent": "security", "action": "dependency_check"},
            {"agent": "performance", "action": "analyze_performance"},
            {"agent": "devops", "action": "monitoring_setup"}
        ]
    },
    "full_security_audit": {
        "description": "Audit de sécurité complet",
        "parallel": False,
        "steps": [
            {"agent": "security", "action": "security_audit"},
            {"agent": "security", "action": "vulnerability_scan"},
            {"agent": "security", "action": "dependency_check"},
            {"agent": "security", "action": "secrets_scan"},
            {"agent": "security", "action": "compliance_check"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "performance_optimization": {
        "description": "Optimisation des performances",
        "parallel": False,
        "steps": [
            {"agent": "performance", "action": "analyze_performance"},
            {"agent": "performance", "action": "find_bottlenecks"},
            {"agent": "performance", "action": "database_optimization"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "performance", "action": "benchmark"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "analyze_project": {
        "description": "Analyser un projet complet",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "analyze_codebase"},
            {"agent": "security", "action": "security_audit"},
            {"agent": "performance", "action": "analyze_performance"},
            {"agent": "tester", "action": "coverage_analysis"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "data_pipeline": {
        "description": "Créer un pipeline de données",
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
        "description": "Déploiement complet avec checks",
        "parallel": False,
        "steps": [
            {"agent": "tester", "action": "run_tests"},
            {"agent": "security", "action": "security_audit"},
            {"agent": "performance", "action": "benchmark"},
            {"agent": "devops", "action": "create_pipeline"},
            {"agent": "devops", "action": "deploy"},
            {"agent": "monitor", "action": "health_check"}
        ]
    },
    "generate_documentation": {
        "description": "Générer documentation complète",
        "parallel": True,
        "steps": [
            {"agent": "documenter", "action": "generate_readme"},
            {"agent": "documenter", "action": "api_docs"},
            {"agent": "documenter", "action": "user_guide"},
            {"agent": "documenter", "action": "changelog"}
        ]
    },
    "infrastructure_review": {
        "description": "Review infrastructure complète",
        "parallel": True,
        "steps": [
            {"agent": "devops", "action": "infrastructure_review"},
            {"agent": "devops", "action": "cost_optimization"},
            {"agent": "security", "action": "compliance_check"},
            {"agent": "performance", "action": "analyze_performance"}
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
            {"agent": "documenter", "action": "generate_report"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "quick_fix": {
        "description": "Correction rapide (bypass review)",
        "parallel": False,
        "steps": [
            {"agent": "debugger", "action": "analyze_error"},
            {"agent": "developer", "action": "fix_bug"},
            {"agent": "devops", "action": "deploy"}
        ]
    },
    "auto_improve": {
        "description": "Amélioration automatique continue",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "analyze_trends"},
            {"agent": "performance", "action": "find_bottlenecks"},
            {"agent": "architect", "action": "propose_improvements"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "tester", "action": "run_tests"},
            {"agent": "devops", "action": "deploy"}
        ]
    }
}

# Quick actions - single agent tasks
QUICK_ACTIONS = {
    "analyze_code": {"agent": "architect", "action": "analyze_codebase"},
    "review_pr": {"agent": "developer", "action": "code_review"},
    "find_bugs": {"agent": "debugger", "action": "find_bugs"},
    "write_tests": {"agent": "tester", "action": "create_tests"},
    "deploy_now": {"agent": "devops", "action": "deploy"},
    "check_health": {"agent": "monitor", "action": "health_check"},
    "analyze_market": {"agent": "trader", "action": "market_analysis"},
    "generate_docs": {"agent": "documenter", "action": "generate_readme"},
    "security_scan": {"agent": "security", "action": "vulnerability_scan"},
    "find_bottlenecks": {"agent": "performance", "action": "find_bottlenecks"},
    "create_pipeline": {"agent": "devops", "action": "create_pipeline"},
    "analyze_data": {"agent": "data", "action": "analyze_data"},
    "create_model": {"agent": "data", "action": "create_model"},
    "cost_optimize": {"agent": "devops", "action": "cost_optimization"},
    "compliance_check": {"agent": "security", "action": "compliance_check"},
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
    "continuous_trading_optimization": {
        "cron": "0 */4 * * *",
        "action": {"agent": "trader", "action": "analyze_performance"}
    },
    "hourly_monitoring": {
        "cron": "0 * * * *",
        "action": {"agent": "monitor", "action": "health_check"}
    }
}
