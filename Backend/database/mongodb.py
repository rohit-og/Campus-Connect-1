"""MongoDB database connection"""

from pymongo import MongoClient
from pymongo.database import Database
from config import MONGODB_URL, MONGODB_DB_NAME

# Create MongoDB client
mongo_client = MongoClient(MONGODB_URL)


def get_mongo_db() -> Database:
    """Get MongoDB database instance"""
    return mongo_client[MONGODB_DB_NAME]
