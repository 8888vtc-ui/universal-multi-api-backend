"""GitHub Provider - Repository and user data"""
import os
import base64
import httpx
from typing import List, Dict, Any, Optional

class GitHubProvider:
    """Provider for GitHub API (free, 5,000 req/hour without auth, 15,000 with auth)"""
    
    def __init__(self):
        self.api_key = os.getenv("GITHUB_API_KEY", "")
        self.base_url = "https://api.github.com"
        self.available = True  # GitHub API works without auth, but with lower rate limits
        if self.api_key and self.api_key != "your_github_token_here":
            print("✅ GitHub provider initialized (free, 15,000 req/hour with auth)")
        else:
            print("✅ GitHub provider initialized (free, 5,000 req/hour without auth)")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers with optional auth"""
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.api_key and self.api_key != "your_github_token_here":
            headers["Authorization"] = f"token {self.api_key}"
        return headers
    
    async def get_user(self, username: str) -> Dict[str, Any]:
        """Get user information"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/users/{username}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def get_user_repos(self, username: str, limit: int = 30) -> List[Dict[str, Any]]:
        """Get user repositories"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self._get_headers(),
                params={"per_page": min(limit, 100), "sort": "updated"}
            )
            response.raise_for_status()
            repos = response.json()
            return repos[:limit]
    
    async def get_repo(self, owner: str, repo: str) -> Dict[str, Any]:
        """Get repository information"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
    
    async def search_repos(self, query: str, limit: int = 30) -> Dict[str, Any]:
        """Search repositories"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/search/repositories",
                headers=self._get_headers(),
                params={"q": query, "per_page": min(limit, 100)}
            )
            response.raise_for_status()
            return response.json()
    
    async def get_repo_readme(self, owner: str, repo: str) -> str:
        """Get repository README content"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{self.base_url}/repos/{owner}/{repo}/readme",
                headers=self._get_headers()
            )
            response.raise_for_status()
            content = response.json()["content"]
            return base64.b64decode(content).decode("utf-8")

