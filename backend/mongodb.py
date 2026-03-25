import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("MONGODB_DB")]
collection = db[os.getenv("MONGODB_COLLECTION")]

# FIXED session (important)
SESSION_ID = os.getenv("SESSION_ID", "default_session")


def save_message(role, content):
    """
    Save each message as a separate MongoDB document
    """
    collection.insert_one({
        "session_id": SESSION_ID,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })


def get_recent_history(limit=20):
    """
    Fetch last N messages for the session (oldest → newest)
    """
    cursor = (
        collection
        .find({"session_id": SESSION_ID})
        .sort("timestamp", -1)
        .limit(limit)
    )

    history = []
    for doc in reversed(list(cursor)):
        history.append({
            "role": doc["role"],
            "content": doc["content"]
        })

    return history
