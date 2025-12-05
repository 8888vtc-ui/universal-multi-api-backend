"""
NASA Space API Provider
All NASA APIs are free and unlimited
"""
import os
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class NASAProvider:
    """NASA Open APIs - Free unlimited access"""
    
    def __init__(self):
        # NASA API key is optional, DEMO_KEY works but has lower rate limits
        self.api_key = os.getenv('NASA_API_KEY', 'DEMO_KEY')
        self.base_url = "https://api.nasa.gov"
        self.available = True
        logger.info("✅ NASA provider initialized")
    
    async def get_apod(self, date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Astronomy Picture of the Day
        date format: YYYY-MM-DD (optional, defaults to today)
        """
        from services.http_client import http_client
        
        url = f"{self.base_url}/planetary/apod"
        params = {'api_key': self.api_key}
        
        if date:
            params['date'] = date
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return {
                'title': data['title'],
                'explanation': data['explanation'],
                'url': data['url'],
                'media_type': data['media_type'],
                'date': data['date'],
                'copyright': data.get('copyright', 'Public Domain')
            }
        except Exception as e:
            logger.error(f"NASA APOD error: {e}")
            raise
    
    async def get_mars_rover_photos(
        self,
        rover: str = 'curiosity',
        sol: int = 1000,
        camera: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get Mars Rover photos
        rover: curiosity, opportunity, spirit
        sol: Martian sol (day)
        camera: FHAZ, RHAZ, MAST, CHEMCAM, MAHLI, MARDI, NAVCAM, PANCAM, MINITES
        """
        from services.http_client import http_client
        
        url = f"{self.base_url}/mars-photos/api/v1/rovers/{rover}/photos"
        params = {
            'api_key': self.api_key,
            'sol': sol
        }
        
        if camera:
            params['camera'] = camera
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            photos = data.get('photos', [])
            
            return {
                'photos': [
                    {
                        'id': photo['id'],
                        'img_src': photo['img_src'],
                        'earth_date': photo['earth_date'],
                        'camera': photo['camera']['full_name'],
                        'rover': photo['rover']['name']
                    }
                    for photo in photos[:20]  # Limit to 20 photos
                ],
                'count': len(photos)
            }
        except Exception as e:
            logger.error(f"NASA Mars Rover error: {e}")
            raise
    
    async def get_neo_feed(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get Near Earth Objects (asteroids)
        Dates format: YYYY-MM-DD
        """
        from services.http_client import http_client
        
        url = f"{self.base_url}/neo/rest/v1/feed"
        
        # Default to last 7 days
        if not start_date:
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'api_key': self.api_key,
            'start_date': start_date,
            'end_date': end_date
        }
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'element_count': data['element_count'],
                'near_earth_objects': data['near_earth_objects']
            }
        except Exception as e:
            logger.error(f"NASA NEO error: {e}")
            raise
    
    async def get_epic_images(self) -> Dict[str, Any]:
        """Get EPIC (Earth Polychromatic Imaging Camera) images"""
        from services.http_client import http_client
        
        url = f"{self.base_url}/EPIC/api/natural"
        params = {'api_key': self.api_key}
        
        try:
            response = await http_client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data:
                return {'images': [], 'count': 0}
            
            # Get latest images
            images = []
            for item in data[:10]:  # Limit to 10
                date = item['date'].split()[0].replace('-', '/')
                image_name = item['image']
                image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date}/png/{image_name}.png"
                
                images.append({
                    'identifier': item['identifier'],
                    'caption': item['caption'],
                    'image_url': image_url,
                    'date': item['date']
                })
            
            return {
                'images': images,
                'count': len(images)
            }
        except Exception as e:
            logger.error(f"NASA EPIC error: {e}")
            raise
