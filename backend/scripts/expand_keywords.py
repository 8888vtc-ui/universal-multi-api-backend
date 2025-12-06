import asyncio
import json
import os
import sys
import re
from typing import List, Dict, Any

# Add project root to path to import services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.expert_config import EXPERTS
from services.ai_router import ai_router

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'data')
KEYWORDS_FILE = os.path.join(FRONTEND_DATA_DIR, 'seo-keywords.json')

def slugify(text: str) -> str:
    """Create a slug from text"""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

async def brainstorm_keywords(expert_id: str, expert_def: Any, existing_slugs: List[str]) -> List[Dict[str, Any]]:
    """Generate new keywords for an expert"""
    print(f"🧠 Brainstorming for {expert_def.name}...")
    
    prompt = f"""
    En tant qu'expert SEO pour WikiAsk, ta mission est de générer 10 nouveaux mots-clés de "longue traîne" qui mettent en avant la valeur ajoutée UNIQUE de WikiAsk : le mélange de **Données Temps Réel** (via API) et d'**Analyse IA**.

    Expert : "{expert_def.name}"
    Description : {expert_def.description}
    Sujets déjà couverts : {', '.join(existing_slugs[:20])}...

    L'objectif est d'expliquer "pourquoi c'est mieux avec l'IA". 
    Exemples de structures recherchées :
    - "Analyse IA [Sujet]" (ex: Analyse IA météo volaille)
    - "Comparatif [Sujet] vs IA"
    - "Pourquoi utiliser l'IA pour [Sujet]"
    - "[Sujet] en temps réel avec explications"
    - "Précision des prévisions [Sujet] par IA"

    Format JSON attendu (liste d'objets) :
    [
        {{
            "fr": "mot clé français axé IA/Data",
            "en": "english keyword focused on AI/Data",
            "volume": "high" | "medium" | "low"
        }}
    ]
    """
    
    try:
        response = await ai_router.route(prompt, preferred_provider="mistral")
        content = response.get("response", "")
        
        # Robust JSON extraction
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            content = match.group(0)
            
        new_keywords = json.loads(content, strict=False)
        
        valid_keywords = []
        for kw in new_keywords:
            slug = slugify(kw['fr'])
            if slug not in existing_slugs:
                kw['slug'] = slug
                valid_keywords.append(kw)
                
        return valid_keywords
        
    except Exception as e:
        print(f"❌ Error brainstorming for {expert_id}: {e}")
        return []

async def main():
    print(f"Loading keywords from {KEYWORDS_FILE}")
    with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    all_existing_slugs = []
    for expert_data in data["experts"].values():
        for kw in expert_data["keywords"]:
            all_existing_slugs.append(kw["slug"])
            
    print(f"Found {len(all_existing_slugs)} existing keywords across all experts.")
    
    total_added = 0
    
    # Process experts concurrently? Maybe too much for the router if we do all at once.
    # Let's do them sequentially or in small batches to be safe.
    
    for expert_id, expert_data in data["experts"].items():
        expert_def = EXPERTS.get(expert_id)
        if not expert_def:
            continue
            
        # Get existing slugs for this expert to avoid redundancy
        expert_slugs = [kw["slug"] for kw in expert_data["keywords"]]
        
        new_kws = await brainstorm_keywords(expert_id, expert_def, expert_slugs)
        
        if new_kws:
            print(f"  ✨ Found {len(new_kws)} new keywords for {expert_def.name}")
            data["experts"][expert_id]["keywords"].extend(new_kws)
            total_added += len(new_kws)
            all_existing_slugs.extend([k['slug'] for k in new_kws]) # Add to ephemeral list
        else:
            print(f"  ⚠️ No new valid keywords found for {expert_def.name}")

    if total_added > 0:
        # Update metadata
        data["metadata"]["totalKeywords"] += total_added
        data["metadata"]["lastUpdated"] = "2024-12-06" # Dynamic date would be better but static for now
        
        with open(KEYWORDS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Successfully added {total_added} new keywords to {KEYWORDS_FILE}")
    else:
        print("\n⏹️ No new keywords added.")

if __name__ == "__main__":
    asyncio.run(main())
