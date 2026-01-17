# Campus Connect AI Engine - Project Structure

## Complete File List

### Core Application Files

| File | Purpose |
|------|---------|
| `main.py` | FastAPI application with all API endpoints |
| `models.py` | Pydantic models for request/response validation |
| `resume_parser.py` | Resume parsing logic (PDF/DOCX to structured data) |
| `ats_engine.py` | ATS scoring engine with multi-criteria evaluation |
| `feedback_generator.py` | Feedback generation for rejected candidates |
| `config.py` | Configuration settings and environment variables |

### Utility & Helper Files

| File | Purpose |
|------|---------|
| `start_server.py` | Convenient startup script for the FastAPI server |
| `example_usage.py` | Example script demonstrating API usage |
| `test_setup.py` | Test script to verify installation and setup |

### Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Complete project documentation |
| `QUICK_START.md` | Quick start guide for getting started |
| `PROJECT_STRUCTURE.md` | This file - project structure overview |
| `LICENSE` | MIT License file |

### Configuration & Setup Files

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies list |
| `ENV_EXAMPLE.txt` | Example environment variables |
| `.gitignore` | Git ignore rules |
| `install.sh` | Installation script for Linux/Mac |
| `install.bat` | Installation script for Windows |

## File Dependencies

```
main.py
├── models.py (imports all data models)
├── resume_parser.py (parses resumes)
├── ats_engine.py (scores resumes)
└── feedback_generator.py (generates feedback)

ats_engine.py
└── models.py (uses ResumeData, JobRequirement)

feedback_generator.py
└── models.py (uses JobRequirement)

resume_parser.py
└── (standalone - uses standard libraries)

config.py
└── (standalone - configuration only)

start_server.py
├── uvicorn (external)
└── main.py (imports app from main)
```

## Directory Structure

```
Campus Connect/
├── main.py                      # FastAPI app entry point
├── models.py                    # Data models
├── resume_parser.py             # Resume parsing
├── ats_engine.py                # ATS scoring
├── feedback_generator.py        # Feedback generation
├── config.py                    # Configuration
├── start_server.py              # Startup script
├── example_usage.py             # Usage examples
├── test_setup.py                # Setup verification
├── requirements.txt             # Dependencies
├── README.md                    # Full documentation
├── QUICK_START.md               # Quick start guide
├── PROJECT_STRUCTURE.md         # This file
├── LICENSE                      # MIT License
├── ENV_EXAMPLE.txt              # Environment variables example
├── .gitignore                   # Git ignore rules
├── install.sh                   # Install script (Linux/Mac)
├── install.bat                  # Install script (Windows)
└── uploads/                     # Upload directory (auto-created)
```

## API Endpoints

All endpoints are defined in `main.py`:

1. `GET /` - API information
2. `GET /health` - Health check
3. `POST /api/v1/evaluate` - Evaluate candidate (form-data)
4. `POST /api/v1/evaluate-json` - Evaluate candidate (JSON)

## Getting Started

1. **Install dependencies:**
   - Windows: `install.bat`
   - Linux/Mac: `./install.sh`
   - Manual: `pip install -r requirements.txt`

2. **Test setup:**
   ```bash
   python test_setup.py
   ```

3. **Start server:**
   ```bash
   python start_server.py
   ```

4. **Access API docs:**
   - http://localhost:8000/docs

5. **Run example:**
   ```bash
   python example_usage.py
   ```

## Key Features

### 1. ATS Resume Screening
- Parses PDF/DOCX resumes
- Multi-criteria scoring (skills, education, experience, keywords, format)
- Configurable minimum score threshold

### 2. Real-time Feedback
- Detailed rejection reasons
- Missing skills identification
- Resume strengths/weaknesses analysis
- Actionable improvement recommendations
- Mistake highlights

## Technology Stack

- **Framework:** FastAPI
- **Language:** Python 3.8+
- **Parsing:** PyPDF2, pdfplumber, python-docx
- **Validation:** Pydantic v2
- **Server:** Uvicorn

## Next Steps

1. Read `QUICK_START.md` for installation
2. Review `README.md` for detailed documentation
3. Check `example_usage.py` for API examples
4. Run `test_setup.py` to verify setup
5. Start developing!


