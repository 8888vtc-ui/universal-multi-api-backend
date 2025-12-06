import urllib.request
import json
import os
import ssl

# Fix for SSL certificate issues
ssl._create_default_https_context = ssl._create_unverified_context

DATA_DIR = r"d:\moteur israelien\frontend\data"

def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(data)} items to {filename}")

# 1. Cryptos (CoinGecko)
print("🚀 Fetching Cryptos...")
try:
    req = urllib.request.Request(
        "https://api.coingecko.com/api/v3/coins/list", 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as url:
        data = json.loads(url.read().decode())
        # Take top 1000
        top_cryptos = data[:1000]
        save_json("cryptos-top200.json", top_cryptos)
except Exception as e:
    print(f"❌ Error fetching cryptos: {e}")

# 2. Cities (Geo API Gouv)
print("🚀 Fetching French Cities...")
try:
    # Fetch all communes with population
    url_str = "https://geo.api.gouv.fr/communes?fields=nom,codesPostaux,population&format=json"
    with urllib.request.urlopen(url_str) as url:
        data = json.loads(url.read().decode())
        # Sort by population desc
        data.sort(key=lambda x: x.get('population', 0), reverse=True)
        # Take top 2500
        top_cities = data[:2500]
        # Format
        formatted_cities = [
            {
                "name": c['nom'], 
                "zip": c['codesPostaux'][0] if c.get('codesPostaux') else "",
                "population": c.get('population', 0)
            } 
            for c in top_cities
        ]
        save_json("cities-fr.json", formatted_cities)
except Exception as e:
    print(f"❌ Error fetching cities: {e}")

# 3. Drugs (OpenFDA)
print("🚀 Fetching Drugs...")
try:
    # OpenFDA count endpoint returns top values
    url_str = "https://api.fda.gov/drug/label.json?count=openfda.brand_name.exact&limit=1000"
    with urllib.request.urlopen(url_str) as url:
        data = json.loads(url.read().decode())
        # data['results'] is a list of { term: "DRUG NAME", count: 123 }
        drugs = [{"name": d['term'].title()} for d in data['results']]
        save_json("drugs-top500.json", drugs)
except Exception as e:
    print(f"❌ Error fetching drugs: {e}")

# 4. Books (OpenLibrary)
print("🚀 Fetching Classic Books...")
try:
    url_str = "https://openlibrary.org/subjects/classic_literature.json?limit=1000"
    with urllib.request.urlopen(url_str) as url:
        data = json.loads(url.read().decode())
        # data['works'] -> title
        books = [
            {
                "title": w['title'], 
                "author": w['authors'][0]['name'] if w.get('authors') else "Unknown"
            } 
            for w in data.get('works', [])
        ]
        save_json("books-classics.json", books)
except Exception as e:
    print(f"❌ Error fetching books: {e}")
