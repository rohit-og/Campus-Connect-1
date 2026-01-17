# Quick Start Guide - Campus Connect AI Engine

## Installation

### Option 1: Automatic Installation (Recommended)

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
chmod +x install.sh
./install.sh
```

### Option 2: Manual Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create uploads directory:**
   ```bash
   mkdir uploads
   ```

## Starting the Server

### Option 1: Using the startup script (Recommended)
```bash
python start_server.py
```

### Option 2: Direct execution
```bash
python main.py
```

### Option 3: Using uvicorn directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the API

Once the server is running (usually on `http://localhost:8000`):

1. **Access API Documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

2. **Run the example script:**
   ```bash
   python example_usage.py
   ```

3. **Test with curl or Postman:**
   - See README.md for API endpoint examples

## Project Structure

```
Campus Connect/
├── main.py                 # FastAPI application
├── models.py               # Pydantic models
├── resume_parser.py        # Resume parsing logic
├── ats_engine.py           # ATS scoring engine
├── feedback_generator.py   # Feedback generation
├── config.py               # Configuration settings
├── start_server.py         # Startup script
├── example_usage.py        # Example usage script
├── requirements.txt        # Python dependencies
├── README.md               # Full documentation
├── QUICK_START.md          # This file
├── LICENSE                 # MIT License
├── install.sh              # Installation script (Linux/Mac)
├── install.bat             # Installation script (Windows)
└── uploads/                # Upload directory (created automatically)
```

## Troubleshooting

### Port already in use
If port 8000 is already in use, change it in `config.py` or set the `API_PORT` environment variable.

### Missing dependencies
Run `pip install -r requirements.txt` again to ensure all packages are installed.

### File upload errors
Ensure the `uploads` directory exists and has write permissions.

### Import errors
Make sure you're running Python 3.8 or higher and all dependencies are installed.

## Need Help?

- Check the full documentation in `README.md`
- Review API documentation at http://localhost:8000/docs
- Check the example usage in `example_usage.py`


