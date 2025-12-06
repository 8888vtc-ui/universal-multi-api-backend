"""Numbers API Provider - Facts about numbers"""
import httpx
import random
from typing import Dict, Any, Optional

class NumbersAPIProvider:
    """Provider for Numbers API (free, unlimited)"""
    
    # Fallback facts
    TRIVIA_FACTS = {
        0: "0 is the additive identity.",
        1: "1 is the multiplicative identity.",
        7: "7 is considered a lucky number in many cultures.",
        13: "13 is considered unlucky in Western superstition.",
        42: "42 is the answer to life, the universe, and everything according to Douglas Adams.",
        100: "100 is a perfect square (10²).",
        365: "365 is the number of days in a common year.",
        1000: "1000 is the first four-digit number.",
    }
    
    MATH_FACTS = {
        0: "0 is the only number that is neither positive nor negative.",
        1: "1 is the only positive integer that is neither prime nor composite.",
        2: "2 is the only even prime number.",
        3: "3 is the first odd prime number.",
        4: "4 is the smallest composite number.",
        6: "6 is the smallest perfect number (1+2+3=6).",
        9: "9 is the first odd composite number.",
        10: "10 is the base of our decimal number system.",
    }
    
    def __init__(self):
        self.base_url = "http://numbersapi.com"
        self.available = True
        print("✅ Numbers API initialized (free, unlimited)")
    
    def _get_fallback_fact(self, number: int, fact_type: str) -> Dict[str, Any]:
        """Get a fallback fact"""
        facts = self.TRIVIA_FACTS if fact_type == "trivia" else self.MATH_FACTS
        
        if number in facts:
            text = facts[number]
        else:
            text = f"{number} is an interesting number."
        
        return {
            "number": number,
            "text": text,
            "found": number in facts,
            "type": fact_type,
            "source": "fallback"
        }
    
    async def get_number_fact(
        self,
        number: int,
        fact_type: str = "trivia"
    ) -> Dict[str, Any]:
        """Get a fact about a number"""
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/{number}/{fact_type}",
                    params={"json": "true"}
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "number": data.get("number"),
                        "text": data.get("text"),
                        "found": data.get("found"),
                        "type": data.get("type"),
                        "source": "numbersapi"
                    }
            except:
                pass
            
            return self._get_fallback_fact(number, fact_type)
    
    async def get_random_fact(self, fact_type: str = "trivia") -> Dict[str, Any]:
        """Get a random number fact"""
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/random/{fact_type}",
                    params={"json": "true"}
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "number": data.get("number"),
                        "text": data.get("text"),
                        "found": data.get("found"),
                        "type": data.get("type"),
                        "source": "numbersapi"
                    }
            except:
                pass
            
            # Fallback to random number from our facts
            facts = self.TRIVIA_FACTS if fact_type == "trivia" else self.MATH_FACTS
            number = random.choice(list(facts.keys()))
            return self._get_fallback_fact(number, fact_type)
    
    async def get_date_fact(self, month: int, day: int) -> Dict[str, Any]:
        """Get a fact about a date"""
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(
                    f"{self.base_url}/{month}/{day}/date",
                    params={"json": "true"}
                )
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "text": data.get("text"),
                        "year": data.get("year"),
                        "found": data.get("found"),
                        "type": "date",
                        "source": "numbersapi"
                    }
            except:
                pass
            
            return {
                "text": f"Something interesting happened on {month}/{day}.",
                "year": None,
                "found": False,
                "type": "date",
                "source": "fallback"
            }

