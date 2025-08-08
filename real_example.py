"""
Real Usage Example - Google Drive Reader
========================================

This shows how to actually use the Google Drive reader with real files.
"""

from src.modules.google_drive_reader import GoogleDriveReader
import json

def real_example():
    """
    Real example of how to use the Google Drive reader
    """
    print("🚀 Real Usage Example")
    print("=" * 40)
    
    # Initialize reader
    reader = GoogleDriveReader()
    
    # Example 1: Process a local file (if you have one)
    print("\n📁 Example 1: Process Local File")
    print("-" * 30)
    
    # Check if there are any files in data/input/
    import os
    input_dir = "data/input"
    if os.path.exists(input_dir):
        files = [f for f in os.listdir(input_dir) if f.endswith(('.pdf', '.docx', '.xlsx', '.csv'))]
        if files:
            print(f"Found files: {files}")
            # Process first file
            file_path = os.path.join(input_dir, files[0])
            try:
                data = reader.process_file(file_path)
                print(f"✅ Processed: {files[0]}")
                print(f"📊 Data extracted: {len(data)} items")
                
                # Show sample of extracted data
                if 'text' in data:
                    print(f"📝 Text pages: {len(data['text'])}")
                if 'tables' in data:
                    print(f"📊 Tables found: {len(data['tables'])}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        else:
            print("No files found in data/input/ directory")
            print("Place your PDF/DOCX/Excel files there to test")
    else:
        print("data/input/ directory not found")
    
    # Example 2: Google Drive URL (you need to provide real URL)
    print("\n📁 Example 2: Google Drive Download")
    print("-" * 30)
    
    # Replace this with your actual Google Drive URL
    # Example: "https://drive.google.com/file/d/1ABC123XYZ/view"
    google_drive_url = input("Enter your Google Drive URL (or press Enter to skip): ").strip()
    
    if google_drive_url:
        try:
            print(f"Downloading from: {google_drive_url}")
            data = reader.download_and_process(google_drive_url)
            print(f"✅ Downloaded and processed successfully!")
            print(f"📊 Files processed: {len(data)}")
            
            # Save extracted data to JSON for inspection
            with open("data/output/extracted_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("💾 Data saved to: data/output/extracted_data.json")
            
        except Exception as e:
            print(f"❌ Error downloading: {e}")
    else:
        print("Skipped Google Drive download")
    
    print("\n✅ Example completed!")
    print("📝 Check data/output/ for extracted data")

if __name__ == "__main__":
    real_example() 