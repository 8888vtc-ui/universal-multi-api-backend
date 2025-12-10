"""Open Trivia Database Provider"""
import httpx
import html
from typing import Dict, Any, List, Optional
from services.http_client import http_client

class OpenTriviaProvider:
    """Provider for Open Trivia Database (free, unlimited)"""
    
    def __init__(self):
        self.base_url = "https://opentdb.com/api.php"
        self.available = True
        print("[OK] Open Trivia DB initialized (free, unlimited)")
    
    async def get_questions(
        self,
        amount: int = 10,
        category: Optional[int] = None,
        difficulty: Optional[str] = None,
        question_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get trivia questions"""
        params = {"amount": amount}
        if category:
            params["category"] = category
        if difficulty:
            params["difficulty"] = difficulty
        if question_type:
            params["type"] = question_type
        
        response = await http_client.get(self.base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Décoder les entités HTML
        questions = []
        for q in data.get("results", []):
            questions.append({
                "category": html.unescape(q.get("category", "")),
                "type": q.get("type"),
                "difficulty": q.get("difficulty"),
                "question": html.unescape(q.get("question", "")),
                "correct_answer": html.unescape(q.get("correct_answer", "")),
                "incorrect_answers": [html.unescape(a) for a in q.get("incorrect_answers", [])]
            })
        
        return {
            "response_code": data.get("response_code"),
            "questions": questions,
            "count": len(questions)
        }
    
    async def get_categories(self) -> List[Dict[str, Any]]:
        """Get available trivia categories"""
        response = await http_client.get("https://opentdb.com/api_category.php")
        response.raise_for_status()
        data = response.json()
        return data.get("trivia_categories", [])






