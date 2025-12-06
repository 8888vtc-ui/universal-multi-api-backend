
import asyncio
import json
import os
import sys
import re
from typing import List, Dict, Any

# Add project root to path to import services
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.expert_config import EXPERTS, ExpertId
from services.ai_router import ai_router

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'data')
KEYWORDS_FILE = os.path.join(FRONTEND_DATA_DIR, 'seo-keywords.json')
ARTICLES_DIR = os.path.join(BASE_DIR, 'data', 'articles')

# Ensure directory exists
os.makedirs(ARTICLES_DIR, exist_ok=True)

async def generate_article_content(expert: Any, keyword: str, lang: str) -> Dict[str, str]:
    """Generate title, excerpt, and content for an article"""
    
    prompt = f"""
    Rédige un article de blog SEO optimisé pour WikiAsk en {lang} sur le sujet : "{keyword}".
    
    L'expert qui rédige est : {expert.name} ({expert.emoji}).
    Description de l'expert : {expert.description}
    Ton : {expert.system_prompt}
    
    Format de réponse attendu (JSON uniquement) :
    {{
        "title": "Titre accrocheur optimisé SEO",
        "excerpt": "Courte description pour les méta-données (150 caractères max)",
        "content": "Contenu complet de l'article en Markdown. Utilise des H2 (##) pour les sections. Inclus une section 'Comment WikiAsk vous aide'.",
        "cta": "Texte court pour le bouton d'appel à l'action (ex: Demander à {expert.name})"
    }}
    
    Règles rédactionnelles :
    1. Contenu informatif, fiable et structuré.
    2. Utilise le Markdown pour le formatage (gras, listes, etc.).
    3. Pas de H1, commence directement par H2.
    4. Mentionne explicitement que WikiAsk utilise l'IA et des sources temps réel.
    5. Sois direct et engageant.
    """
    
    try:
        # Use a high quality provider for better formatting compliance
        response = await ai_router.route(prompt, preferred_provider="mistral") 
        content = response.get("response", "")
        
        # Robust JSON extraction
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        return json.loads(content, strict=False)
    except Exception as e:
        print(f"Error generating content for {keyword} ({lang}): {e}")
        return None

def get_existing_slugs() -> List[str]:
    """Extract slugs from existing JSON files"""
    try:
        return [f.replace(".json", "") for f in os.listdir(ARTICLES_DIR) if f.endswith(".json")]
    except FileNotFoundError:
        return []

async def main():
    print(f"Loading keywords from {KEYWORDS_FILE}")
    with open(KEYWORDS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_slugs = get_existing_slugs()
    print(f"Found {len(existing_slugs)} existing articles in {ARTICLES_DIR}.")
    
    articles_to_generate = []
    
    # Identify missing articles
    for expert_id, expert_data in data.get("experts", {}).items():
        for kw in expert_data.get("keywords", []):
            if kw["slug"] not in existing_slugs:
                articles_to_generate.append({
                    "expert_id": expert_id,
                    "keyword_fr": kw["fr"],
                    "keyword_en": kw["en"],
                    "slug": kw["slug"],
                    "volume": kw["volume"],
                    "data_sources": expert_data.get("dataSources", [])
                })
    
    print(f"Found {len(articles_to_generate)} articles to generate.")
    
    if not articles_to_generate:
        print("All articles already generated!")
        return

    # Process each article
    semaphore = asyncio.Semaphore(5)
    
    async def process_article(idx, total, article):
        async with semaphore:
            slug = article['slug']
            print(f"\n[Starting {idx+1}/{total}] {slug}")
            
            expert_def = EXPERTS.get(article["expert_id"])
            if not expert_def:
                print(f"Expert {article['expert_id']} not found, skipping.")
                return

            # Generate content concurrently
            fr_task = generate_article_content(expert_def, article["keyword_fr"], "fr")
            en_task = generate_article_content(expert_def, article["keyword_en"], "en")
            
            fr_content, en_content = await asyncio.gather(fr_task, en_task)
            
            if not fr_content or not en_content:
                print(f"❌ Failed to generate content for {slug}")
                return

            # Format the entry as pure JSON structure
            article_data = {
                "slug": slug,
                "expertId": article['expert_id'],
                "keywords": [article['keyword_fr'], article['keyword_en']],
                "dataSources": article['data_sources'],
                "date": "2024-12-06",
                "readTime": 5,
                "fr": {
                    "title": fr_content['title'],
                    "excerpt": fr_content['excerpt'],
                    "content": fr_content['content'],
                    "cta": fr_content['cta']
                },
                "en": {
                    "title": en_content['title'],
                    "excerpt": en_content['excerpt'],
                    "content": en_content['content'],
                    "cta": en_content['cta']
                }
            }
            
            # Write to JSON file
            file_path = os.path.join(ARTICLES_DIR, f"{slug}.json")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(article_data, f, indent=2, ensure_ascii=False)
                print(f"✅ Saved {slug} to {file_path}")
            except Exception as e:
                print(f"❌ Error saving {slug}: {e}")

    tasks = [process_article(i, len(articles_to_generate), a) for i, a in enumerate(articles_to_generate)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
