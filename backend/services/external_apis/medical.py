"""
Medical & Health API Providers
PubMed, OpenFDA for medical research and drug information
"""
import httpx
from typing import Dict, Any, List, Optional


class PubMedProvider:
    """PubMed API - Medical research articles (unlimited, free)"""
    
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
        self.available = True
        
    async def search_articles(self, query: str, max_results: int = 10) -> Dict[str, Any]:
        """Search PubMed articles"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                # Step 1: Search for article IDs
                search_response = await client.get(
                    f"{self.base_url}/esearch.fcgi",
                    params={
                        "db": "pubmed",
                        "term": query,
                        "retmax": max_results,
                        "retmode": "json"
                    }
                )
                
                if search_response.status_code != 200:
                    raise Exception(f"PubMed search failed: {search_response.status_code}")
                
                search_data = search_response.json()
                id_list = search_data.get("esearchresult", {}).get("idlist", [])
                
                if not id_list:
                    return {"count": 0, "articles": []}
                
                # Step 2: Fetch article summaries
                summary_response = await client.get(
                    f"{self.base_url}/esummary.fcgi",
                    params={
                        "db": "pubmed",
                        "id": ",".join(id_list),
                        "retmode": "json"
                    }
                )
                
                if summary_response.status_code != 200:
                    raise Exception(f"PubMed summary failed: {summary_response.status_code}")
                
                summary_data = summary_response.json()
                articles = []
                
                for pmid in id_list:
                    article_data = summary_data.get("result", {}).get(pmid, {})
                    articles.append({
                        "pmid": pmid,
                        "title": article_data.get("title", ""),
                        "authors": [author.get("name", "") for author in article_data.get("authors", [])],
                        "source": article_data.get("source", ""),
                        "pub_date": article_data.get("pubdate", ""),
                        "doi": article_data.get("elocationid", "")
                    })
                
                return {
                    "count": len(articles),
                    "articles": articles,
                    "query": query
                }
        
        except Exception as e:
            raise Exception(f"PubMed API error: {e}")


class OpenFDAProvider:
    """OpenFDA API - FDA drug and device data (unlimited, free)"""
    
    def __init__(self):
        self.base_url = "https://api.fda.gov"
        self.available = True
        
    async def search_drugs(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """Search FDA drug database"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/drug/label.json",
                    params={
                        "search": query,
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    drugs = []
                    for result in results:
                        drugs.append({
                            "brand_name": result.get("openfda", {}).get("brand_name", ["N/A"])[0],
                            "generic_name": result.get("openfda", {}).get("generic_name", ["N/A"])[0],
                            "manufacturer": result.get("openfda", {}).get("manufacturer_name", ["N/A"])[0],
                            "purpose": result.get("purpose", ["N/A"])[0] if result.get("purpose") else "N/A",
                            "warnings": result.get("warnings", ["N/A"])[0] if result.get("warnings") else "N/A",
                            "route": result.get("openfda", {}).get("route", ["N/A"])[0]
                        })
                    
                    return {
                        "count": len(drugs),
                        "drugs": drugs,
                        "query": query
                    }
                else:
                    raise Exception(f"OpenFDA returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"OpenFDA API error: {e}")
    
    async def get_adverse_events(self, drug_name: str, limit: int = 10) -> Dict[str, Any]:
        """Get adverse events for a drug"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/drug/event.json",
                    params={
                        "search": f'patient.drug.medicinalproduct:"{drug_name}"',
                        "limit": limit
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "count": len(data.get("results", [])),
                        "events": data.get("results", []),
                        "drug": drug_name
                    }
                else:
                    raise Exception(f"OpenFDA returned status {response.status_code}")
        
        except Exception as e:
            raise Exception(f"OpenFDA API error: {e}")


# Singleton instances
pubmed = PubMedProvider()
openfda = OpenFDAProvider()
