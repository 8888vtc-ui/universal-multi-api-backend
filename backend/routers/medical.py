"""
Medical API Router
Endpoints for medical research and drug information
"""
from fastapi import APIRouter, HTTPException, Query
from services.external_apis import pubmed, openfda

router = APIRouter(prefix="/api/medical", tags=["medical"])


@router.get("/research/search")
async def search_medical_research(
    query: str = Query(..., description="Search query for medical articles"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search PubMed for medical research articles"""
    try:
        data = await pubmed.search_articles(query, max_results)
        return {"success": True, "data": data, "source": "pubmed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drugs/search")
async def search_drugs(
    query: str = Query(..., description="Drug name or condition"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Search FDA drug database"""
    try:
        data = await openfda.search_drugs(query, limit)
        return {"success": True, "data": data, "source": "openfda"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/drugs/adverse-events/{drug_name}")
async def get_adverse_events(
    drug_name: str,
    limit: int = Query(10, ge=1, le=50, description="Maximum number of results")
):
    """Get adverse events for a specific drug"""
    try:
        data = await openfda.get_adverse_events(drug_name, limit)
        return {"success": True, "data": data, "source": "openfda"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
