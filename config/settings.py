"""
Project Configuration Settings
=============================

This file contains all configuration settings for the Report GPT project.
"""

import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
MODELS_DIR = DATA_DIR / "models"

# Create directories if they don't exist
for directory in [DATA_DIR, INPUT_DIR, OUTPUT_DIR, MODELS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Google Drive settings
GOOGLE_DRIVE_SETTINGS = {
    "download_dir": str(INPUT_DIR),
    "supported_extensions": ['.pdf', '.docx', '.xlsx', '.xls', '.csv', '.txt'],
    "max_file_size": 100 * 1024 * 1024,  # 100MB
}

# File processing settings
FILE_PROCESSING = {
    "chunk_size": 1000,  # Characters per chunk for text processing
    "max_pages": 100,     # Maximum pages to process per document
    "table_extraction": True,
    "image_extraction": False,
}

# OpenAI settings (will be added later)
OPENAI_SETTINGS = {
    "api_key": os.getenv("OPENAI_API_KEY", ""),
    "model": "gpt-3.5-turbo",
    "max_tokens": 2000,
    "temperature": 0.7,
}

# Logging settings
LOGGING = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(BASE_DIR / "logs" / "report_gpt.log"),
}

# Report generation settings
REPORT_SETTINGS = {
    "output_formats": ["pdf", "docx", "xlsx"],
    "template_dir": str(BASE_DIR / "templates"),
    "default_template": "standard_report",
}

# Fine-tuning settings (will be added later)
FINE_TUNING = {
    "model_name": "gpt-3.5-turbo",
    "training_data_ratio": 0.8,
    "validation_data_ratio": 0.2,
    "epochs": 3,
    "batch_size": 4,
}

# Database settings (if needed later)
DATABASE = {
    "type": "sqlite",
    "path": str(DATA_DIR / "report_gpt.db"),
}

# Export settings
EXPORT_SETTINGS = {
    "json_indent": 2,
    "csv_encoding": "utf-8",
    "excel_engine": "openpyxl",
} 