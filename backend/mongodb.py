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


def save_message(role, content, session_id):
    collection.insert_one({
        "session_id": session_id,
        "role": role,
        "content": content,
        "timestamp": datetime.utcnow()
    })


def get_recent_history(session_id, limit=20):
    cursor = (
        collection
        .find({"session_id": session_id})
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
