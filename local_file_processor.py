"""
Local File Processor
===================

This script processes local files from data/input/ directory.
You can place your PDF, DOCX, Excel files there and this will process them.
"""

from src.modules.local_file_reader import LocalFileReader
import json
import os
from pathlib import Path

def process_local_files():
    """
    Process all files in data/input/ directory
    """
    print("Local File Processor")
    print("=" * 40)
    
    # Initialize reader
    reader = LocalFileReader()
    
    # Check data/input/ directory
    input_dir = Path("data/input")
    output_dir = Path("data/output")
    output_dir.mkdir(exist_ok=True)
    
    if not input_dir.exists():
        print("❌ data/input/ directory not found!")
        print("📁 Creating data/input/ directory...")
        input_dir.mkdir(parents=True, exist_ok=True)
        print("✅ Directory created!")
        print("\n📋 Instructions:")
        print("1. Copy your files to data/input/ directory")
        print("2. Supported formats: PDF, DOCX, Excel, CSV, TXT")
        print("3. Run this script again")
        return
    
    # Find all supported files (including files without extensions and in subfolders)
    supported_extensions = ['.pdf', '.docx', '.doc', '.xlsx', '.xls', '.csv', '.txt']
    files = []
    
    # Search recursively in all subdirectories
    for file_path in input_dir.rglob('*'):
        if file_path.is_file():
            # Check if file has supported extension
            if file_path.suffix.lower() in supported_extensions:
                files.append(file_path)
            # Also include files without extensions (downloaded files)
            elif file_path.suffix == '':
                files.append(file_path)
    
    if not files:
        print(" No supported files found in data/input/")
        print("\n Supported file types:")
        print("- PDF files (.pdf)")
        print("- Word documents (.docx)")
        print("- Excel files (.xlsx, .xls)")
        print("- CSV files (.csv)")
        print("- Text files (.txt)")
        print("\n Copy your files to data/input/ directory and run again")
        return
    
    print(f" Found {len(files)} files to process:")
    for i, file_path in enumerate(files, 1):
        print(f"  {i}. {file_path.name}")
    
    # Process each file
    all_data = []
    
    for i, file_path in enumerate(files, 1):
        print(f"\n Processing {i}/{len(files)}: {file_path.name}")
        print("-" * 50)
        
        try:
            # Process the file
            data = reader.process_file(str(file_path))
            all_data.append(data)
            
            print(f" Successfully processed: {file_path.name}")
            
            # Show extracted information
            if 'text' in data:
                print(f" Text pages: {len(data['text'])}")
                # Show first few characters of text
                if data['text']:
                    first_text = data['text'][0]['text'][:100] + "..." if len(data['text'][0]['text']) > 100 else data['text'][0]['text']
                    print(f" Sample text: {first_text}")
            
            if 'tables' in data:
                print(f" Tables found: {len(data['tables'])}")
                if data['tables']:
                    print(f" First table has {len(data['tables'][0]['data'])} rows")
            
            if 'sheets' in data:
                print(f" Excel sheets: {list(data['sheets'].keys())}")
                for sheet_name, sheet_data in data['sheets'].items():
                    print(f" {sheet_name}: {len(sheet_data)} rows")
            
            if 'data' in data:  # CSV data
                print(f" CSV rows: {len(data['data'])}")
            
        except Exception as e:
            print(f" Error processing {file_path.name}: {e}")
            continue
    
    # Save all extracted data
    if all_data:
        output_file = output_dir / "extracted_data.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n All data saved to: {output_file}")
        print(f" Total files processed: {len(all_data)}")
        
        # Create summary
        summary = {
            "total_files": len(all_data),
            "files_processed": [data.get('file_path', 'Unknown') for data in all_data],
            "total_text_pages": sum(len(data.get('text', [])) for data in all_data),
            "total_tables": sum(len(data.get('tables', [])) for data in all_data),
            "total_excel_sheets": sum(len(data.get('sheets', {})) for data in all_data),
            "total_csv_rows": sum(len(data.get('data', [])) for data in all_data)
        }
        
        summary_file = output_dir / "processing_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f" Summary saved to: {summary_file}")
        print("\n  Processing Summary:")
        print(f"   Files processed: {summary['total_files']}")
        print(f"   Text pages: {summary['total_text_pages']}")
        print(f"   Tables found: {summary['total_tables']}")
        print(f"   Excel sheets: {summary['total_excel_sheets']}")
        print(f"   CSV rows: {summary['total_csv_rows']}")
    
    print("\nProcessing completed!")
    print("Check data/output/ for extracted data")

def show_instructions():
    """
    Show instructions for using local files
    """
    print("How to Use Local Files:")
    print("=" * 40)
    print("1. Copy your files to data/input/ directory")
    print("2. Run: python local_file_processor.py")
    print("3. Check data/output/ for results")
    print("\nSupported File Types:")
    print("- PDF files (.pdf)")
    print("- Word documents (.docx)")
    print("- Excel files (.xlsx, .xls)")
    print("- CSV files (.csv)")
    print("- Text files (.txt)")
    print("\nExample file structure:")
    print("data/input/")
    print("  report.pdf")
    print("  data.xlsx")
    print("  document.docx")

if __name__ == "__main__":
    show_instructions()
    print("\n" + "="*50)
    process_local_files() 