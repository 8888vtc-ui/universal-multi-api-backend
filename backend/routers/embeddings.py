"""
Embeddings endpoint for RAG system
"""
from fastapi import APIRouter, HTTPException
from models.schemas import EmbeddingRequest, EmbeddingResponse
from services.cache import cache_service
import os
import cohere

router = APIRouter(prefix="/api", tags=["embeddings"])


def get_cohere_client():
    """Get Cohere client"""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key or api_key == "your_cohere_api_key_here":
        return None
    return cohere.Client(api_key)


@router.post("/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    """
    Create embeddings for text (for RAG system)
    
    - **text**: Text to embed (required)
    - **model**: Embedding model (cohere/openai)
    """
    try:
        # Check cache first
        cache_key = f"{request.text}:{request.model}"
        cached = cache_service.get("embeddings", cache_key)
        
        if cached:
            return EmbeddingResponse(**cached)
        
        # Create embeddings based on model
        if request.model == "cohere":
            client = get_cohere_client()
            
            if not client:
                raise HTTPException(
                    status_code=503,
                    detail="Cohere API not configured"
                )
            
            response = client.embed(
                texts=[body.text],
                model="embed-multilingual-v3.0",
                input_type="search_query"
            )
            
            embeddings = response.embeddings[0]
            
            result = {
                "embeddings": embeddings,
                "model": "cohere-embed-multilingual-v3.0",
                "dimensions": len(embeddings)
            }
        
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported model: {body.model}"
            )
        
        # Cache the embeddings
        cache_ttl = int(os.getenv("CACHE_TTL_EMBEDDINGS", 86400))
        cache_service.set(
            "embeddings",
            cache_key,
            result,
            ttl=cache_ttl
        )
        
        return EmbeddingResponse(**result)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Embedding error: {str(e)}"
        )
