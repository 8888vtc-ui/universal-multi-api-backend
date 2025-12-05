"""
Personal AI Assistant Router
Endpoints pour l'assistant personnel IA
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from services.assistant.assistant_router import assistant_router
from services.assistant.memory_store import memory_store

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


class LearnRequest(BaseModel):
    """Request pour apprendre d'une interaction"""
    user_id: str
    query: str
    category: str
    action: str = "search"
    feedback: Optional[str] = None  # positive, negative, neutral


class UpdatePreferenceRequest(BaseModel):
    """Request pour mettre à jour une préférence manuellement"""
    user_id: str
    category: str
    weight: float  # 0.0 à 1.0
    keywords: Optional[List[str]] = None


@router.post("/learn")
async def learn_from_interaction(request: LearnRequest):
    """
    🧠 Apprendre d'une interaction utilisateur
    
    L'assistant apprend de vos interactions pour améliorer ses recommandations.
    
    **Catégories supportées:**
    - finance, news, weather, medical, entertainment, nutrition, etc.
    
    **Actions:**
    - search: Recherche effectuée
    - click: Clic sur un résultat
    - like: Like d'un résultat
    - share: Partage d'un résultat
    """
    try:
        result = await assistant_router.learn_from_interaction(
            user_id=request.user_id,
            query=request.query,
            category=request.category,
            action=request.action,
            feedback=request.feedback
        )
        
        return {
            "success": True,
            **result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_recommendations(
    user_id: str = Query(..., description="ID utilisateur"),
    limit: int = Query(10, ge=1, le=50, description="Nombre de recommandations"),
    categories: Optional[str] = Query(None, description="Catégories séparées par virgule")
):
    """
    💡 Obtenir des recommandations personnalisées
    
    Retourne des recommandations basées sur vos préférences et historique.
    
    **Exemple:**
    - Si vous cherchez souvent "bitcoin", vous recevrez des recommandations finance
    - Si vous lisez beaucoup d'actualités tech, vous recevrez des recommandations news tech
    """
    try:
        category_list = categories.split(",") if categories else None
        
        recommendations = await assistant_router.get_recommendations(
            user_id=user_id,
            limit=limit,
            categories=category_list
        )
        
        return {
            "success": True,
            **recommendations
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preferences/update")
async def update_preference(request: UpdatePreferenceRequest):
    """
    ⚙️ Mettre à jour une préférence manuellement
    
    Permet de définir ou modifier une préférence utilisateur.
    
    **Exemple:**
    - Category: "finance"
    - Weight: 0.9 (très important)
    - Keywords: ["bitcoin", "crypto", "trading"]
    """
    try:
        from services.assistant.preference_learner import preference_learner
        
        preference_learner.update_preference(
            user_id=request.user_id,
            category=request.category,
            weight=request.weight,
            keywords=request.keywords or []
        )
        
        return {
            "success": True,
            "message": f"Préférence {request.category} mise à jour"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{user_id}")
async def get_user_profile(user_id: str):
    """
    👤 Obtenir le profil complet d'un utilisateur
    
    Retourne toutes les informations sur l'utilisateur :
    - Statistiques d'utilisation
    - Préférences apprises
    - Patterns détectés
    - Historique d'interactions
    """
    try:
        profile = assistant_router.get_user_profile(user_id)
        
        return {
            "success": True,
            **profile
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/{user_id}")
async def get_user_stats(user_id: str):
    """
    📊 Obtenir les statistiques d'un utilisateur
    
    Statistiques d'utilisation et d'interactions.
    """
    try:
        stats = memory_store.get_user_stats(user_id)
        
        return {
            "success": True,
            **stats
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/routine/optimize")
async def optimize_routine(
    user_id: str = Query(..., description="ID utilisateur")
):
    """
    ⚡ Optimiser la routine quotidienne
    
    Analyse vos habitudes et suggère des optimisations pour gagner du temps.
    """
    try:
        from services.assistant.automation_engine import automation_engine
        optimization = await automation_engine.optimize_routine(user_id)
        return {"success": True, **optimization}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/routine/analyze")
async def analyze_routine(
    user_id: str = Query(..., description="ID utilisateur"),
    days: int = Query(7, ge=1, le=30, description="Nombre de jours à analyser")
):
    """📊 Analyser la routine utilisateur"""
    try:
        from services.assistant.automation_engine import automation_engine
        analysis = await automation_engine.analyze_routine(user_id, days)
        return {"success": True, **analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task/execute")
async def execute_task(
    user_id: str = Query(..., description="ID utilisateur"),
    task_type: str = Query(..., description="Type de tâche"),
    parameters: Optional[str] = Query(None, description="Paramètres JSON")
):
    """🤖 Exécuter une tâche automatique"""
    try:
        import json
        from services.assistant.task_executor import task_executor
        params = json.loads(parameters) if parameters else {}
        result = await task_executor.execute_task(user_id, task_type, params)
        return {"success": result.get("success", False), **result}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Paramètres JSON invalides")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/available")
async def get_available_tasks():
    """Obtenir la liste des tâches automatiques disponibles"""
    from services.assistant.task_executor import task_executor
    tasks = task_executor.get_available_tasks()
    return {"success": True, "tasks": tasks, "total": len(tasks)}


@router.get("/routine/suggest")
async def suggest_routine(
    user_id: str = Query(..., description="ID utilisateur")
):
    """💡 Suggérer une routine optimale"""
    try:
        from services.assistant.automation_engine import automation_engine
        analysis = await automation_engine.analyze_routine(user_id)
        if not analysis.get("routine_analyzed"):
            return {"success": False, "message": analysis.get("message")}
        optimization = await automation_engine.optimize_routine(user_id)
        most_active_hour = analysis["analysis"].get("most_active_hour")
        routine_suggestions = {"morning": [], "afternoon": [], "evening": []}
        if most_active_hour:
            if 6 <= most_active_hour < 12:
                routine_suggestions["morning"].append("Effectuer recherches importantes le matin")
            elif 12 <= most_active_hour < 18:
                routine_suggestions["afternoon"].append("Période optimale pour recherches")
            else:
                routine_suggestions["evening"].append("Consultation le soir")
        return {
            "success": True,
            "suggested_routine": routine_suggestions,
            "optimization": optimization,
            "analysis": analysis
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_assistant_status():
    """
    ℹ️ Obtenir le statut de l'assistant
    
    Retourne les fonctionnalités disponibles et le statut du service.
    """
    status = assistant_router.get_status()
    return {
        "success": True,
        **status
    }


@router.post("/routine/optimize")
async def optimize_routine(
    user_id: str = Query(..., description="ID utilisateur")
):
    """
    ⚡ Optimiser la routine quotidienne
    
    Analyse vos habitudes et suggère des optimisations pour gagner du temps.
    
    **Retourne:**
    - Analyse de votre routine actuelle
    - Suggestions d'optimisation avec IA
    - Temps potentiellement économisé
    """
    try:
        optimization = await automation_engine.optimize_routine(user_id)
        
        return {
            "success": True,
            **optimization
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/routine/analyze")
async def analyze_routine(
    user_id: str = Query(..., description="ID utilisateur"),
    days: int = Query(7, ge=1, le=30, description="Nombre de jours à analyser")
):
    """
    📊 Analyser la routine utilisateur
    
    Analyse vos interactions pour détecter des patterns de routine.
    """
    try:
        analysis = await automation_engine.analyze_routine(user_id, days)
        
        return {
            "success": True,
            **analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/task/execute")
async def execute_task(
    user_id: str = Query(..., description="ID utilisateur"),
    task_type: str = Query(..., description="Type de tâche (daily_summary, price_alert, etc.)"),
    parameters: Optional[str] = Query(None, description="Paramètres JSON (optionnel)")
):
    """
    🤖 Exécuter une tâche automatique
    
    Exécute une tâche basée sur vos préférences et historique.
    
    **Tâches disponibles:**
    - `daily_summary`: Résumé quotidien de vos activités
    - `price_alert`: Alertes prix pour cryptos/actions suivies
    - `news_digest`: Digest actualités selon vos intérêts
    - `routine_suggestion`: Suggestions pour optimiser routine
    """
    try:
        import json
        params = json.loads(parameters) if parameters else {}
        
        result = await task_executor.execute_task(
            user_id=user_id,
            task_type=task_type,
            parameters=params
        )
        
        return {
            "success": result.get("success", False),
            **result
        }
    
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Paramètres JSON invalides")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tasks/available")
async def get_available_tasks():
    """Obtenir la liste des tâches automatiques disponibles"""
    tasks = task_executor.get_available_tasks()
    return {
        "success": True,
        "tasks": tasks,
        "total": len(tasks)
    }


@router.get("/routine/suggest")
async def suggest_routine(
    user_id: str = Query(..., description="ID utilisateur")
):
    """
    💡 Suggérer une routine optimale
    
    Génère des suggestions pour une routine quotidienne optimale basée sur vos habitudes.
    """
    try:
        # Analyser routine actuelle
        analysis = await automation_engine.analyze_routine(user_id)
        
        if not analysis.get("routine_analyzed"):
            return {
                "success": False,
                "message": analysis.get("message", "Pas assez de données")
            }
        
        # Générer suggestions
        optimization = await automation_engine.optimize_routine(user_id)
        
        # Créer routine suggérée
        routine_suggestions = {
            "morning": [],
            "afternoon": [],
            "evening": []
        }
        
        most_active_hour = analysis["analysis"].get("most_active_hour")
        if most_active_hour:
            if 6 <= most_active_hour < 12:
                routine_suggestions["morning"].append("Effectuer recherches importantes le matin")
            elif 12 <= most_active_hour < 18:
                routine_suggestions["afternoon"].append("Période optimale pour recherches")
            else:
                routine_suggestions["evening"].append("Consultation le soir")
        
        return {
            "success": True,
            "suggested_routine": routine_suggestions,
            "optimization": optimization,
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def assistant_info():
    """
    📚 Informations sur l'assistant personnel IA
    """
    return {
        "service": "Personal AI Assistant",
        "version": "1.0.0",
        "description": "Assistant IA qui apprend de vos interactions et anticipe vos besoins",
        "features": [
            "Apprentissage des préférences",
            "Recommandations personnalisées",
            "Mémoire conversationnelle",
            "Patterns temporels",
            "Automatisation intelligente"
        ],
        "endpoints": {
            "learn": "/api/assistant/learn",
            "recommendations": "/api/assistant/recommendations",
            "profile": "/api/assistant/profile/{user_id}",
            "preferences": "/api/assistant/preferences/update"
        }
    }

