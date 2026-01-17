"""
Setup and Test Helper Script
Automatically installs dependencies and runs tests
"""

import sys
import subprocess

def install_dependencies():
    """Install required dependencies"""
    print("="*60)
    print("Installing Dependencies")
    print("="*60)
    print(f"Python: {sys.executable}")
    print(f"Version: {sys.version}")
    print()
    
    packages = [
        "fastapi>=0.104.1",
        "uvicorn[standard]>=0.24.0",
        "python-multipart>=0.0.6",
        "pydantic>=2.8.0",
        "PyPDF2>=3.0.1",
        "python-docx>=1.1.0",
        "pdfplumber>=0.10.3"
    ]
    
    print("Installing packages...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-q", "--upgrade"
        ] + packages)
        print("[OK] All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[X] Error installing dependencies: {e}")
        return False

def main():
    """Main function"""
    print("\n" + "="*60)
    print("Campus Connect AI Engine - Setup Helper")
    print("="*60)
    
    # Check if packages are installed
    missing = []
    required = ["fastapi", "uvicorn", "pydantic", "PyPDF2", "docx", "pdfplumber"]
    
    for package in required:
        try:
            __import__(package.lower() if package != "PyPDF2" else "PyPDF2")
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        response = input("\nWould you like to install dependencies now? (y/n): ").lower()
        
        if response == 'y':
            if install_dependencies():
                print("\n" + "="*60)
                print("Setup complete! Running test_setup.py...")
                print("="*60 + "\n")
                
                # Run test_setup.py
                import test_setup
            else:
                print("\n[!] Installation failed. Please install manually:")
                print("   pip install -r requirements.txt")
        else:
            print("\n[!] Skipping installation. Please install dependencies manually:")
            print("   pip install -r requirements.txt")
    else:
        print("\n[OK] All dependencies are already installed!")
        print("\n" + "="*60)
        print("Running test_setup.py...")
        print("="*60 + "\n")
        import test_setup

if __name__ == "__main__":
    main()

