# 🤖 AI-Powered Report Generation System

An intelligent system for reading, processing, and generating reports from various document formats using AI fine-tuning.

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)

## ✨ Features

### 🔍 **Document Reading**
- **Google Drive Integration**: Download files and folders directly from Google Drive
- **Local File Processing**: Read files from local directories
- **Multiple Formats**: Support for PDF, DOCX, Excel, CSV, and TXT files
- **Automatic Detection**: Smart file type detection and extension handling

### 📊 **Data Processing**
- **Text Extraction**: Extract text content from documents
- **Table Extraction**: Extract tables and structured data
- **Multi-sheet Support**: Handle Excel files with multiple sheets
- **Structured Output**: JSON format for easy processing

### 🎯 **AI Integration** (Coming Soon)
- **Fine-tuning**: Train custom models on your data
- **Q&A System**: Ask questions about your documents
- **Report Generation**: Generate formatted reports

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Windows/Linux/macOS

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd Report-GPT
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
.\env\Scripts\Activate.ps1
# Linux/Mac:
source env/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment Variables
Create a `.env` file in the root directory:
```env
# Google Drive URLs (Optional)
GOOGLE_DRIVE_FILE_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/YOUR_FOLDER_ID

# OpenAI API (For future use)
OPENAI_API_KEY=your_openai_api_key_here
```

## 🎯 Quick Start

### Option 1: Process Google Drive Files
1. **Add URLs to `.env` file**
2. **Run the system**:
   ```bash
   python example_usage.py
   ```

### Option 2: Process Local Files
1. **Place files in `data/input/` directory**
2. **Run the system**:
   ```bash
   python example_usage.py
   ```

## 📖 Usage Guide

### 🔗 Google Drive Integration

#### Single File Download
```python
from src.modules.google_drive_reader import GoogleDriveReader

# Initialize reader
reader = GoogleDriveReader()

# Download and process single file
file_url = "https://drive.google.com/file/d/YOUR_FILE_ID/view"
data = reader.download_and_process(file_url, is_folder=False)
```

#### Folder Download
```python
# Download and process entire folder
folder_url = "https://drive.google.com/drive/folders/YOUR_FOLDER_ID"
data = reader.download_and_process(folder_url, is_folder=True)
```

### 📁 Local File Processing

#### Process Local Files
```python
from src.modules.local_file_reader import LocalFileReader

# Initialize reader
reader = LocalFileReader()

# Process single file
data = reader.process_file("path/to/your/file.pdf")
```

#### Process Multiple Files
```bash
# Run local file processor
python local_file_processor.py
```

### 📊 Supported File Formats

| Format | Extension | Features |
|--------|-----------|----------|
| **PDF** | `.pdf` | Text + Tables extraction |
| **Word** | `.docx` | Text + Tables extraction |
| **Excel** | `.xlsx`, `.xls` | Multi-sheet data extraction |
| **CSV** | `.csv` | Tabular data extraction |
| **Text** | `.txt` | Plain text extraction |

### 🔧 Configuration

#### Environment Variables
```env
# Google Drive URLs
GOOGLE_DRIVE_FILE_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/YOUR_FOLDER_ID

# OpenAI API (Future use)
OPENAI_API_KEY=your_api_key_here
```

#### Settings Configuration
Edit `config/settings.py` for advanced settings:
```python
# Data directories
INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

# Processing settings
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.xlsx', '.csv', '.txt']
```

## 📁 Project Structure

```
Report-GPT/
├── 📁 src/
│   └── 📁 modules/
│       ├── 🔧 google_drive_reader.py    # Google Drive integration
│       ├── 🔧 local_file_reader.py      # Local file processing
│       └── 🔧 (future modules)          # AI, fine-tuning, etc.
├── 📁 data/
│   ├── 📁 input/                        # Input files directory
│   └── 📁 output/                       # Processed data output
├── 📁 config/
│   └── 🔧 settings.py                   # Project configuration
├── 🔧 example_usage.py                  # Main usage example
├── 🔧 local_file_processor.py           # Local file processor
├── 🔧 requirements.txt                  # Python dependencies
├── 🔧 .env                              # Environment variables
└── 📄 README.md                         # This file
```

## 🔍 Output Format

### JSON Structure
```json
{
  "file_path": "path/to/file.pdf",
  "text": [
    {
      "page": 1,
      "text": "Extracted text content..."
    }
  ],
  "tables": [
    {
      "page": 1,
      "table_num": 1,
      "data": [["Header1", "Header2"], ["Data1", "Data2"]]
    }
  ]
}
```

### Excel Output
```json
{
  "file_path": "path/to/file.xlsx",
  "sheets": {
    "Sheet1": [
      {"Column1": "Value1", "Column2": "Value2"}
    ]
  }
}
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Virtual Environment Issues
```bash
# Recreate virtual environment
python -m venv env --clear
.\env\Scripts\Activate.ps1
pip install -r requirements.txt
```

#### 2. Module Import Errors
```bash
# Check if virtual environment is activated
# Should show: (env) at the start of command prompt
pip list  # Should show installed packages
```

#### 3. Google Drive Download Issues
- **Check URL format**: Must be Google Drive URL
- **File permissions**: Ensure file is publicly accessible
- **Network issues**: Check internet connection

#### 4. File Processing Errors
```bash
# Check file format support
# Ensure file is not corrupted
# Verify file permissions
```

### Error Messages

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'pandas'` | Run `pip install pandas` |
| `Invalid folder URL format` | Use correct Google Drive folder URL |
| `Unsupported file type` | Check file extension and format |
| `UnicodeEncodeError` | File contains special characters |

## 🚀 Advanced Usage

### Custom File Processing
```python
from src.modules.google_drive_reader import GoogleDriveReader

# Initialize with custom directory
reader = GoogleDriveReader(download_dir="custom/path")

# Process with custom settings
data = reader.download_and_process(url, is_folder=False)
```

### Batch Processing
```python
# Process multiple URLs
urls = [
    "https://drive.google.com/file/d/ID1/view",
    "https://drive.google.com/file/d/ID2/view"
]

for url in urls:
    data = reader.download_and_process(url)
    # Process data...
```

## 🔮 Future Features

- **AI Fine-tuning**: Train custom models on your data
- **Q&A System**: Ask questions about documents
- **Report Generation**: Generate formatted reports
- **Web Interface**: User-friendly web UI
- **API Endpoints**: REST API for integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

