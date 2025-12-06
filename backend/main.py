"""
Universal Multi-API Backend v2.4.0
Production-Ready FastAPI Backend with 70+ API integrations
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Setup logging
from services.logging_config import setup_logging, ensure_logging_configured
ensure_logging_configured()

logger = logging.getLogger(__name__)

# Run startup validations
from services.startup_validator import validate_startup
startup_results = validate_startup(fail_on_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Universal Multi-API Backend v2.4.0...")
    
    # Log enabled features
    from services.ai_router import ai_router
    from services.cache import cache_service
    
    ai_status = ai_router.get_status()
    available_ai = [name for name, info in ai_status.items() if info.get("available")]
    logger.info(f"🤖 AI Providers: {', '.join(available_ai) or 'None'}")
    logger.info(f"💾 Cache: {'Redis' if cache_service.available else 'Memory (degraded)'}")
    logger.info(f"✅ Startup validation: {'Passed' if startup_results.get('overall_valid') else 'Warnings'}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    from services.http_client import cleanup_http_client
    await cleanup_http_client()
    
    # Cleanup auth tokens
    try:
        from services.auth import auth_service
        cleaned = auth_service.cleanup_expired_tokens()
        if cleaned:
            logger.info(f"🧹 Cleaned {cleaned} expired tokens")
    except:
        pass
    
    logger.info("✅ Shutdown complete")


# Import routers
from routers import (
    chat, embeddings, health, finance, medical, entertainment,
    translation, news, messaging, weather, space, sports,
    utilities, geocoding, nutrition, email, media, boltai,
    aggregated, search, assistant, analytics, auth, health_check,
    countries, webhooks, wikipedia, giphy, books, omdb, ip_geolocation, youtube,
    jsonplaceholder, randomuser, fakestore, quotes, lorem, pixabay, lorempicsum,
    github, worldtime, coincap, tinyurl,
    # New APIs (December 2024 - Extended)
    jokes, trivia, bored, numbers, animals, exchange, export, openlibrary,
    nameanalysis, history
)
from routers import health_deep, metrics, search_optimized, ai_search

# Video router optionnel (dépendances lourdes)
try:
    from routers import video
    VIDEO_AVAILABLE = True
except ImportError:
    VIDEO_AVAILABLE = False
    logger.warning("⚠️ Video router not available (missing dependencies)")

# Create FastAPI app with lifespan
app = FastAPI(
    title="Universal Multi-API Backend",
    description="""
    ## 🚀 Production-Ready Multi-API Backend
    
    Complete backend with **70+ API integrations**:
    
    ### 🤖 AI & LLM (10 providers)
    Groq, Mistral, Gemini, Anthropic, Cohere, AI21, Perplexity, Hugging Face, OpenRouter, Ollama
    
    ### 💰 Finance & Crypto
    CoinGecko, CoinCap, Alpha Vantage, Yahoo Finance, Exchange Rate API
    
    ### 📰 Media & Content
    NewsAPI, NewsData.io, OMDB (movies), YouTube, Giphy, Pixabay
    
    ### 🌍 Location & Geo
    OpenMeteo, WeatherAPI, REST Countries, IP Geolocation, Nominatim, OpenCage
    
    ### 📚 Knowledge & Data
    Wikipedia, Google Books, Open Library, Open Trivia DB, Numbers API
    
    ### 🎭 Fun & Entertainment
    JokeAPI, Chuck Norris, Bored API, Dog API, Cat API, Lorem Picsum
    
    ### 🔧 Utilities
    TinyURL, Export (JSON/CSV/MD), Name Analysis (Agify/Genderize), Search History
    
    ### 🔍 Intelligent Search
    - **AI Search**: IA + Data combined search
    - **Optimized Search**: Category-based grouping
    - **Universal Search**: Cross-API queries
    
    ### ⚙️ Features
    - Intelligent fallback between providers
    - Redis caching with memory fallback
    - Rate limiting & circuit breaker
    - JWT authentication
    - Request tracing (X-Request-ID)
    - Prometheus metrics
    - Export to JSON/CSV/Markdown
    - Search history tracking
    """,
    version="2.4.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Health", "description": "Health checks and status"},
        {"name": "AI Chat", "description": "AI chat and embeddings"},
        {"name": "Finance", "description": "Crypto, stocks, market data"},
        {"name": "News", "description": "News articles and headlines"},
        {"name": "Weather", "description": "Current weather and forecasts"},
        {"name": "Search", "description": "Universal cross-API search"},
        {"name": "Metrics", "description": "Prometheus metrics"},
    ]
)

# ============================================
# MIDDLEWARE (order matters - last added = first executed)
# ============================================

# 1. CORS (must be first for preflight requests)
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Response-Time", "X-API-Version"]
)

# 2. GZip Compression
from starlette.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=500)

# 3. Security Headers
from middleware.security_headers import SecurityHeadersMiddleware
app.add_middleware(SecurityHeadersMiddleware)

# 4. Request ID (for tracing)
from middleware.request_id import RequestIDMiddleware
app.add_middleware(RequestIDMiddleware)

# 5. Exception Handler
from middleware.exception_handler import ExceptionHandlerMiddleware, http_exception_handler
app.add_middleware(ExceptionHandlerMiddleware)
app.add_exception_handler(HTTPException, http_exception_handler)

# 6. Request Logger (logs all requests with timing)
from middleware.request_logger import RequestLoggerMiddleware
app.add_middleware(RequestLoggerMiddleware)

# 7. Sanitization (detects dangerous inputs)
from middleware.sanitization import SanitizationMiddleware
app.add_middleware(SanitizationMiddleware)

# 8. Rate Limiting
try:
    from slowapi import _rate_limit_exceeded_handler
    from slowapi.errors import RateLimitExceeded
    from services.rate_limiter import limiter
    
    if limiter:
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        
        from slowapi.middleware import SlowAPIMiddleware
        app.add_middleware(SlowAPIMiddleware)
        logger.info("🚦 Rate limiting enabled")
except ImportError:
    logger.warning("⚠️ slowapi not installed - rate limiting disabled")

# ============================================
# ROUTERS
# ============================================

# Health & Status
app.include_router(health.router)
app.include_router(health_check.router)
app.include_router(health_deep.router)
app.include_router(metrics.router)

# AI & Chat
app.include_router(chat.router)
app.include_router(embeddings.router)
app.include_router(boltai.router)
app.include_router(assistant.router)

# Search & Aggregation
app.include_router(search.router)
app.include_router(aggregated.router)
app.include_router(search_optimized.router)
app.include_router(ai_search.router)

# Finance
app.include_router(finance.router)

# Media & Content
app.include_router(news.router)
app.include_router(media.router)
if VIDEO_AVAILABLE:
    app.include_router(video.router)
app.include_router(entertainment.router)

# Location & Weather
app.include_router(weather.router)
app.include_router(geocoding.router)
app.include_router(space.router)

# Communication
app.include_router(messaging.router)
app.include_router(email.router)
app.include_router(translation.router)

# Health & Nutrition
app.include_router(medical.router)
app.include_router(nutrition.router)
app.include_router(sports.router)

# Utilities & Auth
app.include_router(utilities.router)
app.include_router(auth.router)
app.include_router(analytics.router)

# New APIs (December 2024)
app.include_router(countries.router)
app.include_router(webhooks.router)
app.include_router(wikipedia.router)
app.include_router(giphy.router)
app.include_router(books.router)
app.include_router(omdb.router)
app.include_router(ip_geolocation.router)
app.include_router(youtube.router)

# Free APIs (January 2025)
app.include_router(jsonplaceholder.router)
app.include_router(randomuser.router)
app.include_router(fakestore.router)
app.include_router(quotes.router)
app.include_router(lorem.router)
app.include_router(pixabay.router)
app.include_router(lorempicsum.router)
app.include_router(github.router)
app.include_router(worldtime.router)
app.include_router(coincap.router)
app.include_router(tinyurl.router)

# Extended Free APIs (December 2024)
app.include_router(jokes.router)      # JokeAPI + Chuck Norris
app.include_router(trivia.router)     # Open Trivia DB
app.include_router(bored.router)      # Bored API (activities)
app.include_router(numbers.router)    # Numbers API (facts)
app.include_router(animals.router)    # Dog + Cat APIs
app.include_router(exchange.router)   # Exchange Rate API
app.include_router(export.router)     # Export (JSON, CSV, Markdown)
app.include_router(openlibrary.router)  # Open Library (free books)
app.include_router(nameanalysis.router)  # Agify/Genderize/Nationalize
app.include_router(history.router)    # Search History


# ============================================
# ROOT ENDPOINTS
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """
    🏠 Root endpoint with API overview
    """
    from services.ai_router import ai_router
    from services.cache import cache_service
    
    ai_status = ai_router.get_status()
    available_ai = [name for name, info in ai_status.items() if info.get("available")]
    
    return {
        "name": "Universal Multi-API Backend",
        "version": "2.4.0",
        "status": "operational",
        "features": {
            "ai_providers": len(available_ai),
            "cache": "redis" if cache_service.available else "memory",
            "rate_limiting": hasattr(app.state, 'limiter'),
            "security_headers": True,
            "request_tracing": True
        },
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "health_deep": "/api/health/deep",
            "metrics": "/api/metrics",
            "prometheus": "/api/metrics/prometheus"
        }
    }


@app.get("/api/info", tags=["Root"])
async def api_info():
    """
    ℹ️ Detailed API information
    """
    from services.ai_router import ai_router
    from services.cache import cache_service
    
    return {
        "version": "2.4.0",
        "environment": os.getenv("ENVIRONMENT", "development"),
        "python_version": os.sys.version.split()[0],
        "features": {
            "ai": {
                "providers": ai_router.get_status(),
                "available_count": len([
                    name for name, info in ai_router.get_status().items()
                    if info.get("available")
                ])
            },
            "cache": {
                "type": "redis" if cache_service.available else "none",
                "available": cache_service.available
            },
            "security": {
                "rate_limiting": hasattr(app.state, 'limiter'),
                "security_headers": True,
                "cors_enabled": True,
                "request_tracing": True
            }
        },
        "routes_count": len([r for r in app.routes if hasattr(r, 'path')]),
        "startup_validation": startup_results
    }


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    # Fly.io utilise PORT, sinon API_PORT, sinon 8000 par défaut
    port = int(os.getenv("PORT", os.getenv("API_PORT", 8000)))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    workers = int(os.getenv("API_WORKERS", 1))
    
    banner = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║  🚀 Universal Multi-API Backend v2.4.0                           ║
    ║  ═══════════════════════════════════════════════════════════════ ║
    ║  📡 Server:     http://{host}:{port:<5}                              ║
    ║  📚 Docs:       http://{host}:{port}/docs                            ║
    ║  ❤️  Health:     http://{host}:{port}/api/health                     ║
    ║  📊 Metrics:    http://{host}:{port}/api/metrics                     ║
    ║  ═══════════════════════════════════════════════════════════════ ║
    ║  APIs: 70+ (AI | Finance | News | Weather | Jokes | Books...)    ║
    ║  Features: AI Search | Export | History | Fallback | Cache       ║
    ║  Security: JWT | Rate Limit | CORS | Headers | Sanitization      ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
        workers=1 if reload else workers,
        access_log=False  # We use our own request logger
    )
