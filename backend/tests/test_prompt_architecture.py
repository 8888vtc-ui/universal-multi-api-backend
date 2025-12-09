
import sys
import os

# Add parent dir to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.expert_config import EXPERTS, ALWAYS_RESPOND_RULE
from services.provider_personalities import enhance_for_provider, PROVIDER_PERSONALITIES

def test_layer_1_universal_rule():
    print("\n🔹 Testing Layer 1: Universal Rule Injection...")
    all_experts_have_rule = True
    for expert_id, expert in EXPERTS.items():
        if ALWAYS_RESPOND_RULE not in expert.system_prompt:
            print(f"❌ Expert {expert.name} ({expert_id}) MISSING Universal Rule!")
            all_experts_have_rule = False
        else:
            # print(f"✅ Expert {expert.name} has Universal Rule")
            pass
    
    if all_experts_have_rule:
        print("✅ SUCCESS: All experts have the Universal Rule injected.")
    else:
        print("❌ FAILURE: Some experts are missing the rule.")

def test_layer_2_provider_personalities():
    print("\n🔹 Testing Layer 2: Provider Personalities Configuration...")
    if "groq" in PROVIDER_PERSONALITIES and "gemini" in PROVIDER_PERSONALITIES:
        print("✅ SUCCESS: Provider personalities defined.")
        print(f"   Groq: {PROVIDER_PERSONALITIES['groq']}")
        print(f"   Gemini: {PROVIDER_PERSONALITIES['gemini']}")
    else:
        print("❌ FAILURE: Missing keys in PROVIDER_PERSONALITIES")

def test_layer_3_integration():
    print("\n🔹 Testing Layer 3: Integration (Prompt Construction)...")
    
    base_prompt = "Tu es un assistant."
    provider = "gemini"
    
    enhanced = enhance_for_provider(base_prompt, provider)
    
    print(f"   Original: {base_prompt}")
    print(f"   Enhanced:\n---\n{enhanced}\n---")
    
    if f"STYLE {provider.upper()}" in enhanced and PROVIDER_PERSONALITIES[provider] in enhanced:
        print("✅ SUCCESS: Personality correctly applied to prompt.")
    else:
        print("❌ FAILURE: Personality NOT applied.")

if __name__ == "__main__":
    print("🚀 STARTING PROMPT ARCHITECTURE TEST")
    test_layer_1_universal_rule()
    test_layer_2_provider_personalities()
    test_layer_3_integration()
    print("\n🏁 TEST COMPLETE")
