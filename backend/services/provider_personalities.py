
PROVIDER_PERSONALITIES = {
    "groq": "Sois DIRECT et CONCIS. Va droit au but.",
    "gemini": "Sois CRÉATIF et ENGAGEANT. Utilise des analogies.",
    "anthropic": "Sois ANALYTIQUE et DÉTAILLÉ. Approfondis.",
    "mistral": "Sois PRÉCIS et EFFICACE.",
    "openai": "Sois CLAIR et STANDARD.",
    "cohere": "Sois PROFESSIONNEL."
}

def enhance_for_provider(system_prompt: str, provider_name: str) -> str:
    """Add provider-specific personality to system prompt"""
    personality = PROVIDER_PERSONALITIES.get(provider_name.lower())
    # Partial match or direct match
    if not personality:
        for key in PROVIDER_PERSONALITIES:
            if key in provider_name.lower():
                personality = PROVIDER_PERSONALITIES[key]
                break
    
    if personality:
        return f"{system_prompt}\n\n🎨 STYLE {provider_name.upper()}: {personality}"
    
    return system_prompt
