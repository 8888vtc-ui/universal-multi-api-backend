"""
🎯 ORCHESTRATOR - The Brain that coordinates all agents - OPTIMIZED VERSION

OPTIMIZATIONS:
- Parallel task execution
- Automatic health checks
- Priority queue
- WebSocket notifications
- Better error recovery
- Automatic agent restart
"""
import os
import asyncio
import logging
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from github import Github
from collections import defaultdict

from .agents import (
    ArchitectAgent, DeveloperAgent, DebuggerAgent,
    TesterAgent, MonitorAgent, TradingAgent, DocumenterAgent,
    SecurityAgent, PerformanceAgent, DevOpsAgent, DataAgent,
    NotificationAgent, ApiAgent
)
from .agents.config import WORKFLOWS

logger = logging.getLogger(__name__)


class TaskPriority:
    """Task priority levels"""
    CRITICAL = 0  # Execute immediately
    HIGH = 1      # Next in queue
    NORMAL = 2    # Standard processing
    LOW = 3       # Background task


class OrchestratorMetrics:
    """Track orchestrator performance"""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.tasks_processed = 0
        self.workflows_executed = 0
        self.errors = 0
        self.health_checks = 0
        self.uptime_checks = []
    
    @property
    def uptime(self) -> str:
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours}h {minutes}m {seconds}s"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "uptime": self.uptime,
            "tasks_processed": self.tasks_processed,
            "workflows_executed": self.workflows_executed,
            "errors": self.errors,
            "health_checks": self.health_checks,
            "started_at": self.start_time.isoformat()
        }


class Orchestrator:
    """
    Central Intelligence - Coordinates all AI agents - ULTRA EDITION.
    13 specialized agents, Redis cache, all free-tier fallbacks.
    """
    
    HEALTH_CHECK_INTERVAL = 300  # 5 minutes
    MAX_CONCURRENT_TASKS = 8  # Increased for more parallelism
    AUTO_START = True
    
    def __init__(self):
        # Initialize ALL 13 agents
        self.agents = {
            "architect": ArchitectAgent(),
            "developer": DeveloperAgent(),
            "debugger": DebuggerAgent(),
            "tester": TesterAgent(),
            "monitor": MonitorAgent(),
            "trader": TradingAgent(),
            "documenter": DocumenterAgent(),
            "security": SecurityAgent(),
            "performance": PerformanceAgent(),
            "devops": DevOpsAgent(),
            "data": DataAgent(),
            "notification": NotificationAgent(),
            "api": ApiAgent(),
        }
        
        # GitHub connection
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.github = Github(self.github_token) if self.github_token else None
        
        # Task management
        self.data_file = "orchestrator_data.json"
        self._load_data()
        
        # State
        self.running = False
        self.metrics = OrchestratorMetrics()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.last_health_check = None
        
        # Event callbacks (for WebSocket/notifications)
        self.event_callbacks: List[callable] = []
        
        logger.info(f"[Orchestrator] Initialized with {len(self.agents)} agents")

    def _load_data(self):
        """Load tasks from disk"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.task_queue = data.get("queue", [])
                    self.completed_tasks = data.get("completed", [])
                    self.failed_tasks = data.get("failed", [])
            else:
                self.task_queue = []
                self.completed_tasks = []
                self.failed_tasks = []
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            self.task_queue = []
            self.completed_tasks = []
            self.failed_tasks = []

    def _save_data(self):
        """Save tasks to disk"""
        try:
            data = {
                "queue": self.task_queue,
                "completed": self.completed_tasks[-100:],  # Keep last 100
                "failed": self.failed_tasks[-50:],  # Keep last 50
                "last_save": datetime.now().isoformat()
            }
            with open(self.data_file, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """Emit event to all registered callbacks"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        for callback in self.event_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                logger.error(f"Event callback error: {e}")
    
    def register_event_callback(self, callback: callable):
        """Register a callback for orchestrator events"""
        self.event_callbacks.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of orchestrator and all agents"""
        github_status = "disconnected"
        if self.github:
            try:
                user = self.github.get_user()
                github_status = f"connected ({user.login})"
            except:
                github_status = "error"
        
        return {
            "orchestrator": {
                "status": "running" if self.running else "idle",
                "queue_size": len(self.task_queue),
                "completed": len(self.completed_tasks),
                "failed": len(self.failed_tasks),
                "active_tasks": len(self.active_tasks),
                "metrics": self.metrics.to_dict()
            },
            "github": github_status,
            "agents": {
                name: agent.get_status() 
                for name, agent in self.agents.items()
            },
            "last_health_check": self.last_health_check.isoformat() if self.last_health_check else None
        }
    
    async def add_task(self, task: Dict[str, Any], priority: int = TaskPriority.NORMAL) -> Dict[str, Any]:
        """Add a task to the queue with priority"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self.task_queue)}"
        task["id"] = task_id
        task["created_at"] = datetime.now().isoformat()
        task["status"] = "queued"
        task["priority"] = priority
        
        # Insert based on priority
        inserted = False
        for i, queued_task in enumerate(self.task_queue):
            if queued_task.get("priority", TaskPriority.NORMAL) > priority:
                self.task_queue.insert(i, task)
                inserted = True
                break
        
        if not inserted:
            self.task_queue.append(task)
        
        self._save_data()
        
        await self._emit_event("task_added", {"task_id": task_id, "priority": priority})
        logger.info(f"📥 Task added: {task_id} - {task.get('description', 'No description')} (priority: {priority})")
        
        return {"success": True, "task_id": task_id, "queue_position": self.task_queue.index(task)}
    
    async def execute_task_immediately(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task immediately without queuing"""
        agent_name = task.get("agent", "monitor")
        
        if agent_name not in self.agents:
            return {"success": False, "error": f"Agent not found: {agent_name}"}
        
        agent = self.agents[agent_name]
        
        try:
            start_time = datetime.now()
            result = await agent.execute(task)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.metrics.tasks_processed += 1
            
            result["execution_time"] = f"{execution_time:.2f}s"
            result["agent_used"] = agent_name
            
            return result
            
        except Exception as e:
            self.metrics.errors += 1
            return {"success": False, "error": str(e)}
    
    async def execute_workflow(self, workflow_name: str, context: Dict[str, Any], parallel: bool = False) -> Dict[str, Any]:
        """Execute a predefined workflow with optional parallel execution"""
        if workflow_name not in WORKFLOWS:
            return {"success": False, "error": f"Unknown workflow: {workflow_name}"}
        
        workflow = WORKFLOWS[workflow_name]
        logger.info(f"🚀 Starting workflow: {workflow_name} (parallel: {parallel})")
        
        await self._emit_event("workflow_started", {"workflow": workflow_name})
        
        start_time = datetime.now()
        results = []
        
        if parallel:
            # Execute independent steps in parallel
            results = await self._execute_parallel_workflow(workflow, context)
        else:
            # Sequential execution
            for step in workflow["steps"]:
                agent_name = step["agent"]
                action = step["action"]
                
                if agent_name not in self.agents:
                    logger.error(f"Agent not found: {agent_name}")
                    continue
                
                agent = self.agents[agent_name]
                task = {"action": action, **context}
                
                logger.info(f"  → {agent.name}: {action}")
                result = await agent.execute(task)
                results.append({
                    "agent": agent_name,
                    "action": action,
                    "result": result,
                    "success": result.get("success", True)
                })
                
                # Pass result to next step if needed
                if result.get("success"):
                    context.update(result)
                else:
                    # Stop workflow on failure
                    logger.error(f"Workflow stopped due to failure at {agent_name}:{action}")
                    break
        
        execution_time = (datetime.now() - start_time).total_seconds()
        self.metrics.workflows_executed += 1
        
        success = all(r.get("success", True) for r in results)
        
        await self._emit_event("workflow_completed", {
            "workflow": workflow_name,
            "success": success,
            "execution_time": execution_time
        })
        
        logger.info(f"{'✅' if success else '❌'} Workflow complete: {workflow_name} in {execution_time:.2f}s")
        
        return {
            "success": success,
            "workflow": workflow_name,
            "steps": results,
            "execution_time": f"{execution_time:.2f}s"
        }
    
    async def _execute_parallel_workflow(self, workflow: Dict, context: Dict) -> List[Dict]:
        """Execute workflow steps in parallel where possible"""
        steps = workflow["steps"]
        results = []
        
        # Group steps by agent to avoid conflicts
        agent_groups = defaultdict(list)
        for i, step in enumerate(steps):
            agent_groups[step["agent"]].append((i, step))
        
        # Execute each group's first step in parallel
        tasks = []
        for agent_name, agent_steps in agent_groups.items():
            if agent_name in self.agents:
                step = agent_steps[0][1]
                agent = self.agents[agent_name]
                task = {"action": step["action"], **context}
                tasks.append(self._run_agent_task(agent, step, task))
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return [r if not isinstance(r, Exception) else {"success": False, "error": str(r)} for r in results]
    
    async def _run_agent_task(self, agent, step: Dict, task: Dict) -> Dict:
        """Run a single agent task"""
        try:
            result = await agent.execute(task)
            return {
                "agent": step["agent"],
                "action": step["action"],
                "result": result,
                "success": result.get("success", True)
            }
        except Exception as e:
            return {
                "agent": step["agent"],
                "action": step["action"],
                "result": {"error": str(e)},
                "success": False
            }
    
    async def run_health_check(self) -> Dict[str, Any]:
        """Run health check on all agents and systems"""
        logger.info("🏥 Running health check...")
        self.last_health_check = datetime.now()
        self.metrics.health_checks += 1
        
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "agents": {},
            "systems": {},
            "overall": "healthy"
        }
        
        # Check each agent
        for name, agent in self.agents.items():
            agent_health = {
                "status": agent.status,
                "model": agent.model,
                "tasks_completed": len(agent.task_history),
                "metrics": agent.metrics.to_dict() if hasattr(agent, 'metrics') else {}
            }
            
            # Check if agent has high error rate
            if hasattr(agent, 'metrics') and agent.metrics.success_rate < 50:
                agent_health["warning"] = "High error rate"
                health_report["overall"] = "degraded"
            
            health_report["agents"][name] = agent_health
        
        # Check GitHub
        if self.github:
            try:
                self.github.get_rate_limit()
                health_report["systems"]["github"] = "connected"
            except:
                health_report["systems"]["github"] = "error"
                health_report["overall"] = "degraded"
        
        # Check queue size
        if len(self.task_queue) > 50:
            health_report["systems"]["queue"] = "backlogged"
            health_report["overall"] = "degraded"
        else:
            health_report["systems"]["queue"] = f"{len(self.task_queue)} pending"
        
        await self._emit_event("health_check", health_report)
        
        return health_report
    
    async def run_continuous(self):
        """Main loop - runs continuously, processing tasks - OPTIMIZED"""
        self.running = True
        logger.info("🔄 Orchestrator starting continuous mode (OPTIMIZED)...")
        
        # Start health check background task
        health_task = asyncio.create_task(self._health_check_loop())
        
        while self.running:
            try:
                # Process up to MAX_CONCURRENT_TASKS tasks in parallel
                tasks_to_process = []
                
                while self.task_queue and len(tasks_to_process) < self.MAX_CONCURRENT_TASKS:
                    task = self.task_queue.pop(0)
                    task["status"] = "processing"
                    tasks_to_process.append(task)
                
                if tasks_to_process:
                    self._save_data()
                    
                    # Execute tasks in parallel
                    async_tasks = [self._process_task(task) for task in tasks_to_process]
                    results = await asyncio.gather(*async_tasks, return_exceptions=True)
                    
                    # Handle results
                    for task, result in zip(tasks_to_process, results):
                        if isinstance(result, Exception):
                            task["status"] = "failed"
                            task["error"] = str(result)
                            self.failed_tasks.append(task)
                            self.metrics.errors += 1
                        else:
                            task["result"] = result
                            task["status"] = "completed"
                            task["completed_at"] = datetime.now().isoformat()
                            self.completed_tasks.append(task)
                            self.metrics.tasks_processed += 1
                    
                    self._save_data()
                    
                    await self._emit_event("tasks_processed", {
                        "count": len(tasks_to_process),
                        "queue_remaining": len(self.task_queue)
                    })
                
                # Wait before next iteration
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Orchestrator error: {e}")
                self.metrics.errors += 1
                await asyncio.sleep(5)
        
        # Clean up
        health_task.cancel()
        logger.info("🛑 Orchestrator stopped")
    
    async def _process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single task"""
        agent_name = task.get("agent", "monitor")
        
        if agent_name not in self.agents:
            raise ValueError(f"Agent not found: {agent_name}")
        
        return await self.agents[agent_name].execute(task)
    
    async def _health_check_loop(self):
        """Background task for periodic health checks"""
        while self.running:
            try:
                await asyncio.sleep(self.HEALTH_CHECK_INTERVAL)
                await self.run_health_check()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Health check error: {e}")
    
    def stop(self):
        """Stop the orchestrator"""
        self.running = False
        logger.info("Stopping orchestrator...")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific task"""
        # Check queue
        for task in self.task_queue:
            if task.get("id") == task_id:
                return task
        
        # Check completed
        for task in self.completed_tasks:
            if task.get("id") == task_id:
                return task
        
        # Check failed
        for task in self.failed_tasks:
            if task.get("id") == task_id:
                return task
        
        return None
    
    def clear_queue(self):
        """Clear all pending tasks"""
        count = len(self.task_queue)
        self.task_queue = []
        self._save_data()
        logger.info(f"Cleared {count} tasks from queue")
        return {"cleared": count}
    
    def retry_failed_tasks(self) -> int:
        """Retry all failed tasks"""
        count = 0
        for task in self.failed_tasks:
            task["status"] = "queued"
            task["retry_count"] = task.get("retry_count", 0) + 1
            if task["retry_count"] <= 3:  # Max 3 retries
                self.task_queue.append(task)
                count += 1
        
        self.failed_tasks = [t for t in self.failed_tasks if t.get("retry_count", 0) > 3]
        self._save_data()
        logger.info(f"Retrying {count} failed tasks")
        return count


# Global orchestrator instance
orchestrator = Orchestrator()
