"""
 Google Drive Reader
===================================

Script shows how to use the Google Drive Reader module.
"""

from src.modules.google_drive_reader import GoogleDriveReader

from dotenv import load_dotenv
import os

def main():
    """
    Main function to demonstrate Google Drive Reader usage
    """
    print("🚀 Report GPT - Google Drive Reader Example")
    print("=" * 50)
    
    # Load .env file
    load_dotenv()
    
    # Initialize the reader
    reader = GoogleDriveReader()
    
    # Example 1: Download and process a single file
    print("\n Downloading Single File")
    print("-" * 30)
    
    # Get URL from .env
    example_file_url = os.getenv("GOOGLE_DRIVE_FILE_URL")
    
    if example_file_url:
        print(f" Processing Google Drive file...")
        try:
            data = reader.download_and_process(example_file_url, is_folder=False)
            print(f"✅ Downloaded and processed file")
            print(f"📊 Extracted data: {len(data)} items")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("")
    
    # Example 2: Download and process a folder
    print("\n Downloading Folder")
    print("-" * 30)
    
    # Get folder URL from .env
    example_folder_url = os.getenv("GOOGLE_DRIVE_FOLDER_URL")
    
    if example_folder_url:
        print(f" Processing Google Drive folder...")
        try:
            data = reader.download_and_process(example_folder_url, is_folder=True)
            print(f"✅ Downloaded and processed folder")
            print(f"📊 Extracted data: {len(data)} items")
        except Exception as e:
            print(f"❌ Error: {e}")
    else:
        print("")
    
    # Example 3: Process local files automatically
    print("\n Processing Local Files...")
    
    try:
        import subprocess
        import sys
        
        # Run local_file_processor.py
        result = subprocess.run([sys.executable, "local_file_processor.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Local files processed successfully!")
        else:
            print(f"⚠️ Local processing had issues")
    except Exception as e:
        print(f"❌ Error processing local files: {e}")
    
    print("\n✅ All processing completed!")

if __name__ == "__main__":
    main() 