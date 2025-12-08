
"""
Simple anti-hallucination utility.
"""

def enhance_system_prompt_anti_hallucination(system_prompt: str, lang: str = "fr") -> str:
    """
    Enhance system prompt with anti-hallucination instructions.
    NOTE: With the new "Universal Rule", we don't aggressively block "I don't know".
    Instead, we focus on grounding ("groundness").
    """
    
    anti_hallucination_instruction = """
INTEGRITY CHECK:
- If you cite numbers or prices, they must come from context or general knowledge (approximations).
- If you are unsure about a specific real-time fact, clarify it involves an estimation.
- Do NOT invent specific URLs or fake citations.
"""
    return f"{system_prompt}\n\n{anti_hallucination_instruction}"
