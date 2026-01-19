"""MongoDB database connection"""

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from pymongo.database import Database
from fastapi import HTTPException, status
from config import MONGODB_URL, MONGODB_DB_NAME

# Create MongoDB client with timeout
try:
    mongo_client = MongoClient(
        MONGODB_URL,
        serverSelectionTimeoutMS=5000  # 5 second timeout
    )
    # Test connection
    mongo_client.server_info()
except (ServerSelectionTimeoutError, ConnectionFailure) as e:
    mongo_client = None
    print(f"Warning: MongoDB connection failed: {e}. Some features may not work.")


def get_mongo_db() -> Database:
    """Get MongoDB database instance"""
    if mongo_client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB connection failed. Please ensure MongoDB is running."
        )
    try:
        # Test connection
        mongo_client.server_info()
        return mongo_client[MONGODB_DB_NAME]
    except (ServerSelectionTimeoutError, ConnectionFailure) as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"MongoDB connection failed: {str(e)}. Please ensure MongoDB is running."
        )
