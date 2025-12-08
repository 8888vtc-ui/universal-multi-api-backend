
import sys
import os

# Add parent directory to path so we can import routers
sys.path.append(os.getcwd())

print("Checking imports...")

try:
    from routers import (
        chat, embeddings, health, finance, medical, entertainment,
        translation, news, messaging, weather, space, sports,
        utilities, geocoding, nutrition, email, media, boltai,
        aggregated, search, assistant, analytics, auth, health_check,
        countries, webhooks, wikipedia, giphy, books, omdb, ip_geolocation, youtube,
        jsonplaceholder, randomuser, fakestore, quotes, lorem, pixabay, lorempicsum,
        github, worldtime, coincap, tinyurl,
        jokes, trivia, bored, numbers, animals, exchange, export, openlibrary,
        nameanalysis, history, blog,
        travel, events, ai_models
    )
    print("Batch 1 OK")
    
    from routers import health_deep, metrics, search_optimized, ai_search, expert_chat, agent, agent_expert, super_chat, agent_metrics
    print("Batch 2 OK")
    
    print("ALL IMPORTS OK")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
