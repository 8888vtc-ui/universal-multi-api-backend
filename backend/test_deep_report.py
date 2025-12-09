"""Test Deep Research Report Generator"""
import asyncio
from services.smart_medical_router import smart_medical_search
from services.deep_research_report import generate_deep_research_report

async def test_deep_report():
    print("="*70)
    print("TESTING DEEP RESEARCH REPORT GENERATOR")
    print("="*70)
    
    query = "diabete type 2 traitement metformine"
    print(f"\nQuery: {query}")
    print("-"*70)
    
    # Step 1: Get medical data
    print("\n1. Fetching data from 77 APIs...")
    context, result = await smart_medical_search(query)
    
    print(f"   Topics detected: {result.detected_topics}")
    print(f"   APIs called: {len(result.apis_called)}")
    print(f"   APIs with data: {len(result.apis_with_data)}")
    print(f"   Time: {result.total_time_ms:.0f}ms")
    
    # Step 2: Generate report
    print("\n2. Generating 3000+ word report...")
    report = await generate_deep_research_report(query, result)
    
    # Count words
    word_count = len(report.split())
    
    print(f"\n   Report generated!")
    print(f"   Word count: {word_count} words")
    print(f"   Minimum required: 3000 words")
    print(f"   Status: {'PASS' if word_count >= 3000 else 'NEED MORE'}")
    
    # Show report preview
    print("\n" + "="*70)
    print("REPORT PREVIEW (first 2000 chars):")
    print("="*70)
    print(report[:2000])
    print("\n... [TRUNCATED] ...")
    
    # Save full report
    with open("DEEP_REPORT_TEST.md", "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nFull report saved to: DEEP_REPORT_TEST.md")
    
    print("\n" + "="*70)
    print("TEST COMPLETE!")
    print("="*70)
    
    return word_count >= 3000

if __name__ == "__main__":
    success = asyncio.run(test_deep_report())
    print(f"\nFinal Result: {'SUCCESS' if success else 'NEEDS IMPROVEMENT'}")
