# 🚀 New Laptop Setup Guide

## 📋 Complete Checklist for New Laptop

### **Step 1: Transfer Files**
Copy these files/folders to your new laptop:

#### **Essential Files:**
```
✅ src/modules/
   ├── google_drive_reader.py
   └── local_file_reader.py

✅ config/
   └── settings.py

✅ Scripts:
   ├── example_usage.py
   ├── local_file_processor.py
   ├── quick_setup.py
   └── requirements.txt

✅ Documentation:
   ├── README.md
   ├── conversation_backup.md
   └── NEW_LAPTOP_SETUP.md (this file)

✅ Configuration:
   └── .env (if you have URLs)
```

#### **Optional Files:**
```
📁 data/ (if you have processed data)
📄 .gitignore
```

---

### **Step 2: Environment Setup**

#### **2.1 Install Python**
- Download Python 3.8+ from python.org
- Add Python to PATH during installation

#### **2.2 Create Virtual Environment**
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# Windows:
.\env\Scripts\Activate.ps1
# Linux/Mac:
source env/bin/activate
```

#### **2.3 Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **Step 3: Quick Setup (Recommended)**

#### **3.1 Run Quick Setup Script**
```bash
python quick_setup.py
```

This script will:
- ✅ Check Python version
- ✅ Create directories
- ✅ Check virtual environment
- ✅ Install dependencies
- ✅ Test imports
- ✅ Test local file processor
- ✅ Create .env template
- ✅ Generate setup summary

#### **3.2 Verify Setup**
```bash
# Test local file processor
python local_file_processor.py

# Test with Google Drive (if URLs in .env)
python example_usage.py
```

---

### **Step 4: Configuration**

#### **4.1 Environment Variables**
Edit `.env` file:
```env
# Google Drive URLs (Optional)
GOOGLE_DRIVE_FILE_URL=https://drive.google.com/file/d/YOUR_FILE_ID/view
GOOGLE_DRIVE_FOLDER_URL=https://drive.google.com/drive/folders/YOUR_FOLDER_ID

# OpenAI API (For future use)
OPENAI_API_KEY=your_openai_api_key_here
```

#### **4.2 Add Test Files**
Place some test files in `data/input/`:
- PDF files (.pdf)
- Word documents (.docx)
- Excel files (.xlsx, .xls)
- CSV files (.csv)
- Text files (.txt)

---

### **Step 5: Testing**

#### **5.1 Test Local Files**
```bash
python local_file_processor.py
```

**Expected Output:**
```
Local File Processor
========================================
Found X files to process:
  1. your_file.pdf
  2. your_file.docx

Processing 1/X: your_file.pdf
--------------------------------------------------
Successfully processed: your_file.pdf
Text pages: 5
Sample text: Your extracted text...

All data saved to: data\output\extracted_data.json
```

#### **5.2 Test Google Drive (Optional)**
```bash
python example_usage.py
```

**Expected Output:**
```
Report GPT - Google Drive Reader Example
==================================================

Processing Google Drive file...
✅ Downloaded and processed file
📊 Extracted data: 1 items

Processing Local Files...
✅ Local files processed successfully!

✅ All processing completed!
```

---

### **Step 6: Verify Results**

#### **6.1 Check Output Files**
```bash
# Check extracted data
type data\output\extracted_data.json

# Check processing summary
type data\output\processing_summary.json
```

#### **6.2 Expected File Structure**
```
Report-GPT/
├── 📁 src/modules/
│   ├── 🔧 google_drive_reader.py
│   └── 🔧 local_file_reader.py
├── 📁 data/
│   ├── 📁 input/          # Your files here
│   └── 📁 output/         # Processed results
├── 📁 config/
│   └── 🔧 settings.py
├── 🔧 example_usage.py
├── 🔧 local_file_processor.py
├── 🔧 quick_setup.py
├── 🔧 requirements.txt
├── 🔧 .env
├── 📄 README.md
├── 📄 conversation_backup.md
└── 📄 NEW_LAPTOP_SETUP.md
```

---

### **Step 7: Troubleshooting**

#### **7.1 Common Issues**

**Issue: Virtual Environment Not Activated**
```bash
# Solution: Activate virtual environment
.\env\Scripts\Activate.ps1
```

**Issue: ModuleNotFoundError**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue: Permission Denied**
```bash
# Solution: Run as administrator or check file permissions
```

**Issue: Python Not Found**
```bash
# Solution: Add Python to PATH or use full path
C:\Python39\python.exe quick_setup.py
```

#### **7.2 Verification Commands**
```bash
# Check Python version
python --version

# Check virtual environment
echo $env:VIRTUAL_ENV  # Windows
echo $VIRTUAL_ENV      # Linux/Mac

# Check installed packages
pip list

# Test imports
python -c "import pandas, requests, pathlib; print('All imports successful')"
```

---

### **Step 8: Next Steps**

#### **8.1 Current Status**
- ✅ Document Reading & Processing (Complete)
- 🔄 AI Fine-tuning (Next Phase)
- 🔄 Report Generation (Next Phase)

#### **8.2 Ready for Development**
```bash
# Start working on next phase
# 1. Report Processor Module
# 2. Fine-tuning Module
# 3. Q&A System
# 4. Report Generator
```

---

### **Step 9: Backup & Sync**

#### **9.1 Important Files to Backup**
```
📁 src/modules/          # Core modules
📄 requirements.txt       # Dependencies
📄 .env                  # Configuration
📄 README.md            # Documentation
📄 conversation_backup.md # Complete history
```

#### **9.2 Git Repository (Optional)**
```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: AI Report Generation System"

# Add remote repository
git remote add origin <your-repo-url>
git push -u origin main
```

---

## 🎯 Success Criteria

### **✅ Setup Complete When:**
- [ ] Python 3.8+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Directories created
- [ ] Local file processor working
- [ ] Google Drive integration working (if URLs provided)
- [ ] Output files generated
- [ ] No error messages

### **🚀 Ready for Next Phase When:**
- [ ] All tests pass
- [ ] Data extraction working
- [ ] Environment stable
- [ ] Documentation complete

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review `conversation_backup.md` for similar issues
3. Check `setup_summary.json` for system status
4. Run `quick_setup.py` for diagnostics

---

**🎉 Congratulations! Your AI-Powered Report Generation System is ready!**

*Setup Guide created on: 2024*  
*Project: AI-powered Report Generation System*  
*Phase: 1 Complete - Ready for Phase 2* 