"""
🤖 AGENT DEFINITIONS - OPTIMIZED VERSION
Each agent has a specific role and uses the best AI model for that task.

OPTIMIZATIONS:
- More detailed capabilities
- Smart model selection (cost vs quality)
- New workflows for automation
- Parallel workflow support
"""

AGENTS = {
    "architect": {
        "name": "🏗️ Architect Agent",
        "model": "gpt-4o",
        "fallbacks": ["groq-llama3", "deepseek-coder"],
        "role": "Analyse les projets, crée les spécifications techniques, planifie les tâches",
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
        "role": "Crée et exécute les tests, vérifie la qualité, teste les UI",
        "capabilities": ["create_tests", "run_tests", "visual_testing", "qa_review", "coverage_analysis"],
        "priority": 3,
        "cost_tier": "premium"
    },
    "reviewer": {
        "name": "📝 Code Reviewer Agent",
        "model": "claude-3.5-sonnet", 
        "fallbacks": ["gpt-4o", "deepseek-coder"],
        "role": "Review le code, vérifie la sécurité, suggère des améliorations",
        "capabilities": ["code_review", "security_audit", "best_practices", "documentation", "performance_review"],
        "priority": 3,
        "cost_tier": "premium"
    },
    "deployer": {
        "name": "🚀 Deployer Agent",
        "model": "groq-llama3",
        "fallbacks": ["gpt-4o-mini", "deepseek-coder"],
        "role": "Déploie les applications, gère les environnements, monitore",
        "capabilities": ["deploy", "rollback", "monitor", "health_check", "configure_env"],
        "priority": 4,
        "cost_tier": "standard"
    },
    "monitor": {
        "name": "📊 Monitor Agent",
        "model": "groq-llama3",
        "fallbacks": ["gpt-4o-mini", "deepseek-coder"],
        "role": "Surveille les logs, détecte les anomalies, alerte en temps réel",
        "capabilities": ["watch_logs", "detect_anomalies", "send_alerts", "report", "trend_analysis"],
        "priority": 1,
        "cost_tier": "standard"
    },
    "trader": {
        "name": "📈 Trading Agent",
        "model": "gpt-4o",
        "fallbacks": ["claude-3.5-sonnet", "groq-llama3"],
        "role": "Analyse les marchés, optimise les stratégies trading, surveille les positions",
        "capabilities": ["market_analysis", "strategy_optimization", "position_monitoring", "risk_management", "backtest"],
        "priority": 1,
        "cost_tier": "premium"
    },
    "documenter": {
        "name": "📚 Documentation Agent",
        "model": "groq-llama3",
        "fallbacks": ["gpt-4o-mini", "claude-3.5-sonnet"],
        "role": "Génère la documentation, README, guides utilisateur",
        "capabilities": ["generate_readme", "api_docs", "user_guide", "changelog", "tutorials"],
        "priority": 4,
        "cost_tier": "standard"
    }
}

# Workflow definitions - how agents collaborate
WORKFLOWS = {
    "fix_bug": {
        "description": "Corriger un bug détecté",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "detect_anomaly"},
            {"agent": "debugger", "action": "analyze_error"},
            {"agent": "developer", "action": "fix_bug"},
            {"agent": "tester", "action": "verify_fix"},
            {"agent": "reviewer", "action": "approve_fix"},
            {"agent": "deployer", "action": "deploy_fix"}
        ]
    },
    "new_feature": {
        "description": "Implémenter une nouvelle feature",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "create_specs"},
            {"agent": "developer", "action": "implement_feature"},
            {"agent": "tester", "action": "create_tests"},
            {"agent": "reviewer", "action": "code_review"},
            {"agent": "documenter", "action": "generate_docs"},
            {"agent": "deployer", "action": "deploy"}
        ]
    },
    "optimize_trading": {
        "description": "Optimiser les bots de trading",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "collect_metrics"},
            {"agent": "trader", "action": "analyze_performance"},
            {"agent": "architect", "action": "propose_improvements"},
            {"agent": "developer", "action": "implement_changes"},
            {"agent": "tester", "action": "backtest"},
            {"agent": "deployer", "action": "deploy"}
        ]
    },
    "daily_maintenance": {
        "description": "Maintenance quotidienne automatique",
        "parallel": True,
        "steps": [
            {"agent": "monitor", "action": "health_check"},
            {"agent": "tester", "action": "run_tests"},
            {"agent": "reviewer", "action": "security_audit"},
            {"agent": "deployer", "action": "report"}
        ]
    },
    "analyze_project": {
        "description": "Analyser un projet complet",
        "parallel": False,
        "steps": [
            {"agent": "architect", "action": "analyze_codebase"},
            {"agent": "reviewer", "action": "security_audit"},
            {"agent": "tester", "action": "coverage_analysis"},
            {"agent": "documenter", "action": "generate_report"}
        ]
    },
    "quick_fix": {
        "description": "Correction rapide (bypass review)",
        "parallel": False,
        "steps": [
            {"agent": "debugger", "action": "analyze_error"},
            {"agent": "developer", "action": "fix_bug"},
            {"agent": "tester", "action": "quick_test"},
            {"agent": "deployer", "action": "deploy_hotfix"}
        ]
    },
    "security_audit": {
        "description": "Audit de sécurité complet",
        "parallel": True,
        "steps": [
            {"agent": "reviewer", "action": "security_audit"},
            {"agent": "debugger", "action": "vulnerability_scan"},
            {"agent": "tester", "action": "penetration_test"},
            {"agent": "architect", "action": "security_report"}
        ]
    },
    "performance_optimization": {
        "description": "Optimisation des performances",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "collect_metrics"},
            {"agent": "debugger", "action": "find_bottlenecks"},
            {"agent": "architect", "action": "propose_optimizations"},
            {"agent": "developer", "action": "implement_optimizations"},
            {"agent": "tester", "action": "benchmark"},
            {"agent": "deployer", "action": "deploy"}
        ]
    },
    "generate_documentation": {
        "description": "Générer la documentation complète",
        "parallel": True,
        "steps": [
            {"agent": "documenter", "action": "generate_readme"},
            {"agent": "documenter", "action": "api_docs"},
            {"agent": "documenter", "action": "user_guide"},
            {"agent": "architect", "action": "architecture_diagram"}
        ]
    },
    "auto_improve": {
        "description": "Amélioration automatique continue",
        "parallel": False,
        "steps": [
            {"agent": "monitor", "action": "analyze_trends"},
            {"agent": "architect", "action": "identify_improvements"},
            {"agent": "developer", "action": "implement_improvements"},
            {"agent": "tester", "action": "regression_test"},
            {"agent": "reviewer", "action": "approve_changes"},
            {"agent": "deployer", "action": "gradual_rollout"}
        ]
    }
}

# Quick actions - single agent tasks
QUICK_ACTIONS = {
    "analyze_code": {"agent": "architect", "action": "analyze_codebase"},
    "review_pr": {"agent": "reviewer", "action": "code_review"},
    "find_bugs": {"agent": "debugger", "action": "find_bugs"},
    "write_tests": {"agent": "tester", "action": "create_tests"},
    "deploy_now": {"agent": "deployer", "action": "deploy"},
    "check_health": {"agent": "monitor", "action": "health_check"},
    "analyze_market": {"agent": "trader", "action": "market_analysis"},
    "generate_docs": {"agent": "documenter", "action": "generate_readme"},
}

# Scheduled tasks - run automatically
SCHEDULED_TASKS = {
    "morning_health_check": {
        "cron": "0 8 * * *",  # Every day at 8 AM
        "workflow": "daily_maintenance"
    },
    "nightly_security_scan": {
        "cron": "0 2 * * *",  # Every day at 2 AM
        "workflow": "security_audit"
    },
    "weekly_performance_review": {
        "cron": "0 10 * * 1",  # Every Monday at 10 AM
        "workflow": "performance_optimization"
    },
    "continuous_trading_optimization": {
        "cron": "0 */4 * * *",  # Every 4 hours
        "action": {"agent": "trader", "action": "analyze_performance"}
    }
}
