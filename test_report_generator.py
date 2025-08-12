"""
Test Report Generator
====================

This script tests the Report Generator with different report types.
"""

import json
from pathlib import Path
from src.modules.report_generator import ReportGenerator

def test_report_generator():
    """
    Test the Report Generator
    """
    print("🧪 Testing Report Generator")
    print("=" * 50)
    
    try:
        # Initialize Report Generator
        print("\n📁 Initializing Report Generator...")
        report_gen = ReportGenerator()
        print("✅ Report Generator initialized successfully")
        
        # Test 1: System stats
        print("\n📊 Step 1: System Statistics...")
        stats = report_gen.get_report_stats()
        print(f"   Model: {stats['model']}")
        print(f"   Training Q&A pairs: {stats['training_data_qa_pairs']}")
        print(f"   Extracted documents: {stats['extracted_documents']}")
        print(f"   API Key: {'✅ Set' if stats['api_key_set'] else '❌ Not set'}")
        
        # Test 2: Generate Executive Summary
        print("\n📝 Step 2: Generating Executive Summary...")
        print("   🤔 Creating executive summary...")
        executive_summary = report_gen.generate_executive_summary()
        
        if 'error' not in executive_summary:
            print(f"   ✅ Executive summary generated successfully")
            print(f"   📊 Tokens used: {executive_summary.get('tokens_used', 'N/A')}")
            print(f"   📄 Word count: {executive_summary.get('word_count', 'N/A')}")
            
            # Save executive summary
            summary_file = report_gen.save_report(executive_summary)
            print(f"   💾 Saved to: {summary_file}")
        else:
            print(f"   ❌ Error: {executive_summary.get('error', 'Unknown error')}")
        
        # Test 3: Generate Key Findings Report
        print("\n🔍 Step 3: Generating Key Findings Report...")
        print("   🤔 Creating key findings report...")
        key_findings = report_gen.generate_key_findings_report()
        
        if 'error' not in key_findings:
            print(f"   ✅ Key findings report generated successfully")
            print(f"   📊 Tokens used: {key_findings.get('tokens_used', 'N/A')}")
            print(f"   📄 Word count: {key_findings.get('word_count', 'N/A')}")
            
            # Save key findings
            findings_file = report_gen.save_report(key_findings)
            print(f"   💾 Saved to: {findings_file}")
        else:
            print(f"   ❌ Error: {key_findings.get('error', 'Unknown error')}")
        
        # Test 4: Generate Recommendations Report
        print("\n💡 Step 4: Generating Recommendations Report...")
        print("   🤔 Creating recommendations report...")
        recommendations = report_gen.generate_recommendations_report()
        
        if 'error' not in recommendations:
            print(f"   ✅ Recommendations report generated successfully")
            print(f"   📊 Tokens used: {recommendations.get('tokens_used', 'N/A')}")
            print(f"   📄 Word count: {recommendations.get('word_count', 'N/A')}")
            
            # Save recommendations
            rec_file = report_gen.save_report(recommendations)
            print(f"   💾 Saved to: {rec_file}")
        else:
            print(f"   ❌ Error: {recommendations.get('error', 'Unknown error')}")
        
        # Test 5: Generate Comprehensive Report
        print("\n📋 Step 5: Generating Comprehensive Report...")
        print("   🤔 Creating comprehensive report...")
        comprehensive = report_gen.generate_comprehensive_report()
        
        if 'error' not in comprehensive:
            print(f"   ✅ Comprehensive report generated successfully")
            print(f"   📊 Total tokens used: {comprehensive.get('total_tokens', 'N/A')}")
            print(f"   📄 Total word count: {comprehensive.get('total_word_count', 'N/A')}")
            
            # Save comprehensive report
            comp_file = report_gen.save_report(comprehensive)
            print(f"   💾 Saved to: {comp_file}")
        else:
            print(f"   ❌ Error: {comprehensive.get('error', 'Unknown error')}")
        
        # Test 6: Show results summary
        print("\n📈 Step 6: Results Summary...")
        total_tokens = 0
        total_words = 0
        successful_reports = 0
        
        reports = [executive_summary, key_findings, recommendations]
        for report in reports:
            if 'error' not in report:
                successful_reports += 1
                total_tokens += report.get('tokens_used', 0)
                total_words += report.get('word_count', 0)
        
        print(f"   Total reports generated: {successful_reports}/3")
        print(f"   Total tokens used: {total_tokens}")
        print(f"   Total words generated: {total_words}")
        print(f"   Average tokens per report: {total_tokens // successful_reports if successful_reports > 0 else 0}")
        
        # Test 7: Show sample content
        print("\n📝 Step 7: Sample Report Content...")
        if 'error' not in executive_summary:
            print(f"\n   📄 Executive Summary Preview:")
            content = executive_summary.get('content', '')
            print(f"   {content[:200]}...")
        
        print("\n✅ Report Generator test completed successfully!")
        print("\n🚀 Ready to generate professional reports!")
        print("   Available report types:")
        print("   - Executive Summary")
        print("   - Key Findings")
        print("   - Recommendations")
        print("   - Comprehensive Report")
        
    except Exception as e:
        print(f"❌ Error testing Report Generator: {e}")
        print("💡 Make sure:")
        print("1. Training dataset exists (run test_report_processor.py first)")
        print("2. OpenAI API key is set in .env file")
        print("3. All dependencies are installed")

if __name__ == "__main__":
    test_report_generator()
