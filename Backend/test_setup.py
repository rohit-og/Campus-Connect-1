"""
Test script to verify Campus Connect AI Engine setup
Checks if all dependencies are installed and imports work correctly
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import fastapi
        print("[OK] FastAPI")
    except ImportError as e:
        print(f"[X] FastAPI - {e}")
        return False
    
    try:
        import uvicorn
        print("[OK] Uvicorn")
    except ImportError as e:
        print(f"[X] Uvicorn - {e}")
        return False
    
    try:
        import pydantic
        print("[OK] Pydantic")
    except ImportError as e:
        print(f"[X] Pydantic - {e}")
        return False
    
    try:
        import PyPDF2
        print("[OK] PyPDF2")
    except ImportError as e:
        print(f"[X] PyPDF2 - {e}")
        return False
    
    try:
        import docx
        print("[OK] python-docx")
    except ImportError as e:
        print(f"[X] python-docx - {e}")
        return False
    
    try:
        import pdfplumber
        print("[OK] pdfplumber")
    except ImportError as e:
        print(f"[X] pdfplumber - {e}")
        return False
    
    
    return True

def test_project_modules():
    """Test if project modules can be imported"""
    print("\nTesting project modules...")
    
    try:
        from models import JobRequirement, ResumeData
        print("[OK] models.py")
    except ImportError as e:
        print(f"[X] models.py - {e}")
        return False
    
    try:
        from resume_parser import ResumeParser
        print("[OK] resume_parser.py")
    except ImportError as e:
        print(f"[X] resume_parser.py - {e}")
        return False
    
    try:
        from ats_engine import ATSEngine
        print("[OK] ats_engine.py")
    except ImportError as e:
        print(f"[X] ats_engine.py - {e}")
        return False
    
    try:
        from feedback_generator import FeedbackGenerator
        print("[OK] feedback_generator.py")
    except ImportError as e:
        print(f"[X] feedback_generator.py - {e}")
        return False
    
    try:
        import config
        print("[OK] config.py")
    except ImportError as e:
        print(f"[X] config.py - {e}")
        return False
    
    return True

def test_directories():
    """Test if required directories exist or can be created"""
    print("\nTesting directories...")
    import os
    
    uploads_dir = "uploads"
    if not os.path.exists(uploads_dir):
        try:
            os.makedirs(uploads_dir)
            print(f"[OK] Created {uploads_dir} directory")
        except Exception as e:
            print(f"[X] Could not create {uploads_dir} directory - {e}")
            return False
    else:
        print(f"[OK] {uploads_dir} directory exists")
    
    return True

def test_python_version():
    """Test Python version"""
    print("\nTesting Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    print(f"Python executable: {sys.executable}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("[X] Python 3.8 or higher is required")
        return False
    
    print("[OK] Python version is compatible")
    return True

if __name__ == "__main__":
    print("="*60)
    print("Campus Connect AI Engine - Setup Test")
    print("="*60)
    print()
    
    all_tests_passed = True
    
    # Test Python version
    if not test_python_version():
        all_tests_passed = False
    
    # Test dependencies
    if not test_imports():
        all_tests_passed = False
        print("\n[!] Some dependencies are missing.")
        print(f"[!] Python interpreter: {sys.executable}")
        print("\nTo install dependencies, run:")
        print(f"  {sys.executable} -m pip install -r requirements.txt")
        print("\nOr use the setup helper:")
        print("  python setup_and_test.py")
    
    # Test project modules
    if not test_project_modules():
        all_tests_passed = False
    
    # Test directories
    if not test_directories():
        all_tests_passed = False
    
    print("\n" + "="*60)
    if all_tests_passed:
        print("[OK] All tests passed! Setup is complete.")
        print("\nYou can now start the server with:")
        print("  python start_server.py")
        print("  or")
        print("  python main.py")
    else:
        print("[X] Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Make sure you're using Python 3.8 or higher")
        print("  3. Check that all project files are in the same directory")
    print("="*60)

