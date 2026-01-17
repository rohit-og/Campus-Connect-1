# IDE Setup Guide - Fixing ModuleNotFoundError

## Problem
If you're seeing `ModuleNotFoundError: No module named 'pydantic'` or similar errors, it means your IDE (Cursor/VS Code) is using a different Python interpreter than the one where packages are installed.

## Solution 1: Install Dependencies in Current Python (Recommended)

Run this command to install dependencies in whatever Python your IDE is using:

```bash
python -m pip install -r requirements.txt
```

Or if that doesn't work, use:

```bash
python -m pip install fastapi uvicorn[standard] python-multipart "pydantic>=2.8.0" PyPDF2 python-docx pdfplumber
```

## Solution 2: Configure IDE to Use Python 3.14.0

If you have Python 3.14.0 installed and it has the packages:

1. **In VS Code/Cursor:**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Python: Select Interpreter"
   - Choose `C:\Python314\python.exe` (or the path to Python 3.14.0)

2. **Or create a `.vscode/settings.json` file:**
   ```json
   {
       "python.defaultInterpreterPath": "C:\\Python314\\python.exe"
   }
   ```

## Solution 3: Use Virtual Environment (Best Practice)

Create a virtual environment in your project:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Then configure IDE to use: .venv\Scripts\python.exe (Windows) or venv/bin/python (Linux/Mac)
```

## Quick Test

Run the setup helper script:

```bash
python setup_and_test.py
```

This will automatically detect missing packages and install them in the current Python interpreter.

## Verify Setup

After installing, run:

```bash
python test_setup.py
```

All tests should pass with `[OK]` status.

## Troubleshooting

- **If packages still don't install:** Make sure you're using the same Python that your IDE is using
- **Check Python version:** `python --version` should match what your IDE shows
- **Check installation location:** `python -m pip list` should show installed packages

