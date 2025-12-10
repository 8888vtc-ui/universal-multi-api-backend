"""
API-Sports Provider
100 requests/day free
"""
import os
import httpx
from typing import Dict, Any, Optional
from services.http_client import http_client


class APISports:
    """API-Sports - Multi-sport data API"""
    
    def __init__(self):
        self.api_key = os.getenv('APISPORTS_KEY')
        if not self.api_key:
            raise ValueError("APISPORTS_KEY not found")
        
        self.base_url = "https://v3.football.api-sports.io"
        self.available = True
    
    async def get_live_matches(self) -> Dict[str, Any]:
        """Get live football matches"""
        url = f"{self.base_url}/fixtures"
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        params = {'live': 'all'}
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'matches': data.get('response', []),
            'count': len(data.get('response', []))
        }
    
    async def get_league_standings(self, league_id: int, season: int) -> Dict[str, Any]:
        """Get league standings"""
        url = f"{self.base_url}/standings"
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        params = {
            'league': league_id,
            'season': season
        }
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        return {
            'standings': data.get('response', []),
            'league': league_id,
            'season': season
        }
    
    async def get_team_info(self, team_id: int) -> Dict[str, Any]:
        """Get team information"""
        url = f"{self.base_url}/teams"
        headers = {
            'x-rapidapi-key': self.api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        params = {'id': team_id}
        
        response = await http_client.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if data.get('response'):
            team = data['response'][0]
            return {
                'team': team.get('team', {}),
                'venue': team.get('venue', {})
            }
        return {}
