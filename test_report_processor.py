"""
Test Report Processor Module
===========================

This script tests the Report Processor Module with existing document data.
"""

import json
from pathlib import Path
from src.modules.report_processor import ReportProcessor
from src.modules.local_file_reader import LocalFileReader

def test_report_processor():
    """
    Test the Report Processor Module
    """
    print("🧪 Testing Report Processor Module")
    print("=" * 50)
    
    # Initialize components
    reader = LocalFileReader()
    processor = ReportProcessor()
    
    # Test with existing data
    print("\n📁 Loading existing processed data...")
    
    try:
        # Load existing extracted data
        with open("data/output/extracted_data.json", "r", encoding="utf-8") as f:
            existing_data = json.load(f)
        
        print(f"✅ Loaded {len(existing_data)} documents")
        
        # Process each document
        processed_documents = []
        
        for i, doc_data in enumerate(existing_data):
            print(f"\n📄 Processing document {i+1}/{len(existing_data)}")
            
            # Process document
            processed_doc = processor.process_document(doc_data)
            
            if processed_doc:
                processed_documents.append(processed_doc)
                
                # Print summary
                summary = processed_doc.get('text_summary', {})
                print(f"   📊 Pages: {summary.get('total_pages', 0)}")
                print(f"   📋 Tables: {summary.get('total_tables', 0)}")
                print(f"   ❓ Q&A Pairs: {summary.get('total_qa_pairs', 0)}")
                
                # Print sections found
                sections = processed_doc.get('sections', {})
                if sections:
                    print(f"   📑 Sections: {', '.join(sections.keys())}")
                
                # Print metrics found
                metrics = processed_doc.get('metrics', {})
                if metrics:
                    print(f"   📈 Metrics: {', '.join(metrics.keys())}")
            else:
                print(f"   ❌ Failed to process document")
        
        # Save processed data
        if processed_documents:
            print(f"\n💾 Saving processed data...")
            
            # Save individual processed documents
            for i, doc in enumerate(processed_documents):
                filename = f"processed_doc_{i+1}_{Path(doc.get('file_path', 'unknown')).stem}.json"
                processor.save_processed_data(doc, filename)
            
            # Create training dataset
            print(f"\n🎯 Creating training dataset...")
            training_data = processor.create_training_dataset(processed_documents)
            
            if training_data:
                # Save training dataset
                training_file = processor.output_dir / "training_dataset.json"
                with open(training_file, 'w', encoding='utf-8') as f:
                    json.dump(training_data, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Training dataset saved to: {training_file}")
                print(f"📊 Total Q&A pairs: {training_data['metadata']['total_qa_pairs']}")
                print(f"📄 Total documents: {training_data['metadata']['total_documents']}")
            else:
                print("❌ Failed to create training dataset")
        
        print(f"\n✅ Report Processor test completed!")
        print(f"📁 Check 'data/output/' for processed files")
        
    except FileNotFoundError:
        print("❌ No existing data found. Please run document processing first.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_report_processor()
