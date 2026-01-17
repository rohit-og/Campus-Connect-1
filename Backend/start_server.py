"""
Startup script for Campus Connect AI Engine
Convenient way to start the FastAPI server
"""

import uvicorn
import os
from config import API_HOST, API_PORT, API_RELOAD

if __name__ == "__main__":
    # Create uploads directory if it doesn't exist
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
        print(f"Created {upload_dir} directory")
    
    print("="*60)
    print("Campus Connect AI Engine - Starting Server")
    print("="*60)
    print(f"Server will run on: http://{API_HOST}:{API_PORT}")
    print(f"API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print(f"Alternative Docs: http://{API_HOST}:{API_PORT}/redoc")
    print("="*60)
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_RELOAD,
        log_level="info"
    )


