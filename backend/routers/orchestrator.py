"""
🤖 ORCHESTRATOR API ROUTER - OPTIMIZED VERSION
Exposes agent capabilities via REST API.

NEW FEATURES:
- Priority queue support
- Task status tracking
- Retry mechanism
- Health check endpoint
- Metrics endpoint
- WebSocket support (prepared)
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from enum import IntEnum
from services.orchestrator import orchestrator, TaskPriority

router = APIRouter(prefix="/api/orchestrator", tags=["Orchestrator"])


class PriorityLevel(IntEnum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3


class TaskRequest(BaseModel):
    agent: str = Field(default="monitor", description="Agent to execute the task")
    action: str = Field(..., description="Action to perform")
    description: Optional[str] = Field(None, description="Human-readable description")
    data: Optional[Dict[str, Any]] = Field(default={}, description="Task data")
    priority: Optional[PriorityLevel] = Field(default=PriorityLevel.NORMAL, description="Task priority")


class WorkflowRequest(BaseModel):
    workflow: str = Field(..., description="Workflow name to execute")
    context: Optional[Dict[str, Any]] = Field(default={}, description="Workflow context data")
    parallel: Optional[bool] = Field(default=False, description="Execute steps in parallel where possible")


class AnalyzeRequest(BaseModel):
    repo: str = Field(..., description="GitHub repository in owner/repo format")
    deep_analysis: Optional[bool] = Field(default=False, description="Perform deep analysis")


@router.get("/status")
async def get_orchestrator_status() -> Dict[str, Any]:
    """
    Get comprehensive status of the orchestrator and all agents
    """
    return orchestrator.get_status()


@router.get("/metrics")
async def get_orchestrator_metrics() -> Dict[str, Any]:
    """
    Get detailed performance metrics
    """
    return {
        "orchestrator": orchestrator.metrics.to_dict(),
        "agents": {
            name: agent.metrics.to_dict() if hasattr(agent, 'metrics') else {}
            for name, agent in orchestrator.agents.items()
        }
    }


@router.get("/agents")
async def list_agents() -> Dict[str, Any]:
    """
    List all available agents and their capabilities
    """
    from services.agents.config import AGENTS
    
    agents_info = {}
    for name, agent in orchestrator.agents.items():
        config = AGENTS.get(name, {})
        agents_info[name] = {
            "name": agent.name,
            "model": agent.model,
            "role": agent.role,
            "status": agent.status,
            "capabilities": config.get("capabilities", []),
            "cost_tier": config.get("cost_tier", "standard"),
            "metrics": agent.metrics.to_dict() if hasattr(agent, 'metrics') else {}
        }
    return {"agents": agents_info, "count": len(agents_info)}


@router.post("/task")
async def submit_task(request: TaskRequest) -> Dict[str, Any]:
    """
    Submit a task to the priority queue
    """
    task = {
        "agent": request.agent,
        "action": request.action,
        "description": request.description,
        **request.data
    }
    return await orchestrator.add_task(task, priority=request.priority)


@router.post("/task/execute")
async def execute_task_now(request: TaskRequest) -> Dict[str, Any]:
    """
    Execute a task immediately (synchronous, bypasses queue)
    """
    if request.agent not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent not found: {request.agent}")
    
    task = {
        "action": request.action,
        **request.data
    }
    return await orchestrator.execute_task_immediately(task | {"agent": request.agent})


@router.get("/task/{task_id}")
async def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    Get status of a specific task by ID
    """
    task = orchestrator.get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task not found: {task_id}")
    return task


@router.post("/workflow")
async def execute_workflow(request: WorkflowRequest) -> Dict[str, Any]:
    """
    Execute a predefined workflow
    """
    return await orchestrator.execute_workflow(
        request.workflow, 
        request.context,
        parallel=request.parallel
    )


@router.get("/workflows")
async def list_workflows() -> Dict[str, Any]:
    """
    List all available workflows with details
    """
    from services.agents.config import WORKFLOWS, QUICK_ACTIONS
    
    return {
        "workflows": {
            name: {
                "description": wf["description"],
                "steps": len(wf["steps"]),
                "parallel": wf.get("parallel", False),
                "agents_involved": list(set(s["agent"] for s in wf["steps"]))
            }
            for name, wf in WORKFLOWS.items()
        },
        "quick_actions": QUICK_ACTIONS
    }


@router.post("/start")
async def start_orchestrator(background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Start the orchestrator in continuous mode
    """
    if orchestrator.running:
        return {"status": "already running", "metrics": orchestrator.metrics.to_dict()}
    
    background_tasks.add_task(orchestrator.run_continuous)
    return {"status": "started", "message": "Orchestrator is now running in continuous mode"}


@router.post("/stop")
async def stop_orchestrator() -> Dict[str, Any]:
    """
    Stop the orchestrator gracefully
    """
    orchestrator.stop()
    return {"status": "stopped", "final_metrics": orchestrator.metrics.to_dict()}


@router.get("/queue")
async def get_task_queue(
    limit: int = Query(default=20, ge=1, le=100)
) -> Dict[str, Any]:
    """
    Get current task queue and recent history
    """
    return {
        "queue": orchestrator.task_queue[:limit],
        "queue_total": len(orchestrator.task_queue),
        "completed": orchestrator.completed_tasks[-limit:],
        "completed_total": len(orchestrator.completed_tasks),
        "failed": orchestrator.failed_tasks[-limit:],
        "failed_total": len(orchestrator.failed_tasks)
    }


@router.delete("/queue")
async def clear_task_queue() -> Dict[str, Any]:
    """
    Clear all pending tasks from queue
    """
    return orchestrator.clear_queue()


@router.post("/retry-failed")
async def retry_failed_tasks() -> Dict[str, Any]:
    """
    Retry all failed tasks (max 3 retries per task)
    """
    count = orchestrator.retry_failed_tasks()
    return {"retried": count, "message": f"{count} tasks added back to queue"}


@router.get("/health")
async def run_health_check() -> Dict[str, Any]:
    """
    Run immediate health check on all systems
    """
    return await orchestrator.run_health_check()


@router.post("/analyze")
async def analyze_repository(request: AnalyzeRequest) -> Dict[str, Any]:
    """
    Quick action: Analyze a GitHub repository
    """
    task = {
        "agent": "architect",
        "action": "analyze_codebase",
        "repo": request.repo,
        "deep": request.deep_analysis
    }
    
    if request.deep_analysis:
        # Run full workflow
        return await orchestrator.execute_workflow("analyze_project", {"repo": request.repo})
    else:
        # Quick analysis
        return await orchestrator.execute_task_immediately(task)


@router.post("/quick/{action_name}")
async def execute_quick_action(
    action_name: str,
    data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Execute a predefined quick action
    """
    from services.agents.config import QUICK_ACTIONS
    
    if action_name not in QUICK_ACTIONS:
        raise HTTPException(
            status_code=404, 
            detail=f"Quick action not found: {action_name}. Available: {list(QUICK_ACTIONS.keys())}"
        )
    
    action = QUICK_ACTIONS[action_name]
    task = {
        "agent": action["agent"],
        "action": action["action"],
        **(data or {})
    }
    
    return await orchestrator.execute_task_immediately(task)


@router.post("/agents/{agent_name}/reset-metrics")
async def reset_agent_metrics(agent_name: str) -> Dict[str, Any]:
    """
    Reset metrics for a specific agent
    """
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_name}")
    
    agent = orchestrator.agents[agent_name]
    if hasattr(agent, 'reset_metrics'):
        agent.reset_metrics()
        return {"status": "reset", "agent": agent_name}
    else:
        return {"status": "not_supported", "agent": agent_name}


@router.get("/agents/{agent_name}/history")
async def get_agent_history(
    agent_name: str,
    limit: int = Query(default=10, ge=1, le=50)
) -> Dict[str, Any]:
    """
    Get task history for a specific agent
    """
    if agent_name not in orchestrator.agents:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_name}")
    
    agent = orchestrator.agents[agent_name]
    return {
        "agent": agent_name,
        "history": agent.task_history[-limit:],
        "total_tasks": len(agent.task_history)
    }
