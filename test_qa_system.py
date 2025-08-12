"""
Test Q&A System
===============

This script tests the Q&A System with sample questions.
"""

import json
from pathlib import Path
from src.modules.qa_system import QASystem

def test_qa_system():
    """
    Test the Q&A System
    """
    print("🧪 Testing Q&A System")
    print("=" * 50)
    
    try:
        # Initialize Q&A System
        print("\n📁 Initializing Q&A System...")
        qa_system = QASystem()
        print("✅ Q&A System initialized successfully")
        
        # Test 1: System stats
        print("\n📊 Step 1: System Statistics...")
        stats = qa_system.get_system_stats()
        print(f"   Model: {stats['model']}")
        print(f"   Training Q&A pairs: {stats['training_data_qa_pairs']}")
        print(f"   Documents: {stats['training_data_documents']}")
        print(f"   Pages: {stats['training_data_pages']}")
        print(f"   Tables: {stats['training_data_tables']}")
        print(f"   API Key: {'✅ Set' if stats['api_key_set'] else '❌ Not set'}")
        
        # Test 2: Sample questions
        print("\n❓ Step 2: Testing Sample Questions...")
        
        sample_questions = [
            "What is the main topic of the ANGOSTURA report?",
            "What are the key findings in the documents?",
            "What methodology was used in the study?",
            "What are the main recommendations?",
            "How many pages are in the documents?"
        ]
        
        print(f"   Testing {len(sample_questions)} questions...")
        
        # Process questions
        results = []
        for i, question in enumerate(sample_questions, 1):
            print(f"\n   Question {i}: {question}")
            print("   🤔 Processing...")
            
            result = qa_system.ask_question(question)
            results.append(result)
            
            print(f"   💡 Answer: {result['answer'][:100]}...")
            print(f"   📊 Tokens: {result.get('tokens_used', 'N/A')}")
        
        # Test 3: Save conversation
        print("\n💾 Step 3: Saving Conversation...")
        conversation_file = qa_system.save_conversation(results)
        print(f"   ✅ Conversation saved to: {conversation_file}")
        
        # Test 4: Show results summary
        print("\n📈 Step 4: Results Summary...")
        total_tokens = sum(r.get('tokens_used', 0) for r in results)
        print(f"   Total questions: {len(results)}")
        print(f"   Total tokens used: {total_tokens}")
        print(f"   Average tokens per question: {total_tokens // len(results) if results else 0}")
        
        # Test 5: Show sample answers
        print("\n📝 Step 5: Sample Answers...")
        for i, result in enumerate(results[:2], 1):  # Show first 2
            print(f"\n   Q{i}: {result['question']}")
            print(f"   A{i}: {result['answer'][:200]}...")
        
        print("\n✅ Q&A System test completed successfully!")
        print("\n🚀 Ready to use!")
        print("   Run: python -c \"from src.modules.qa_system import QASystem; QASystem().interactive_mode()\"")
        
    except Exception as e:
        print(f"❌ Error testing Q&A System: {e}")
        print("💡 Make sure:")
        print("1. Training dataset exists (run test_report_processor.py first)")
        print("2. OpenAI API key is set in .env file")
        print("3. All dependencies are installed")

if __name__ == "__main__":
    test_qa_system()
