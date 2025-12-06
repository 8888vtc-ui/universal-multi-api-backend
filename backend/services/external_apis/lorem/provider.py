"""Lorem Ipsum Provider - Generate placeholder text"""
import httpx
from typing import Dict, Any, Optional

class LoremIpsumProvider:
    """Provider for Lorem Ipsum API (free, unlimited)"""
    
    # Standard Lorem Ipsum text for fallback
    LOREM_IPSUM = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
    
    PARAGRAPHS = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.",
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores.",
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit.",
        "Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam.",
    ]
    
    def __init__(self):
        self.available = True
        print("✅ Lorem Ipsum provider initialized (free, unlimited)")
    
    async def get_text(self, paragraphs: int = 1, words: Optional[int] = None) -> str:
        """Get Lorem Ipsum text"""
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Try external API first
            try:
                response = await client.get(
                    "https://baconipsum.com/api/",
                    params={"type": "all-meat", "paras": paragraphs, "format": "text"}
                )
                if response.status_code == 200:
                    return response.text.strip()
            except:
                pass
            
            # Fallback to predefined text
            result = []
            for i in range(min(paragraphs, len(self.PARAGRAPHS))):
                result.append(self.PARAGRAPHS[i % len(self.PARAGRAPHS)])
            
            # If more paragraphs needed, repeat
            while len(result) < paragraphs:
                result.extend(self.PARAGRAPHS[:paragraphs - len(result)])
            
            return "\n\n".join(result[:paragraphs])
    
    async def get_json(self, paragraphs: int = 1) -> Dict[str, Any]:
        """Get Lorem Ipsum as JSON"""
        text = await self.get_text(paragraphs)
        return {"text": text, "paragraphs": paragraphs, "source": "lorem_ipsum"}

