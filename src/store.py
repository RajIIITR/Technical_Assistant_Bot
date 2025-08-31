from pymongo import MongoClient
from typing import Dict
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """
    Get MongoDB connection using your exact code.
    
    Returns:
        collection: MongoDB collection object
    """
    # Fixed connection string (password '@' → '%40')
    uri = os.getenv("CLUSTER_KEY")
    
    # Connect to MongoDB Atlas
    client = MongoClient(uri)
    
    # Create or connect to database
    db = client["hiring_assistant"]
    
    # Create or connect to collection
    candidates = db["candidate_info"]
    
    return candidates


def save_candidate(candidate_data: Dict):
    """
    Save candidate to MongoDB.
    
    Args:
        candidate_data: Dictionary containing candidate information
    """
    candidates = get_db_connection()
    
    # Insert candidate
    result = candidates.insert_one(candidate_data)
    print("✅ Candidate inserted successfully!")
    
    return str(result.inserted_id)


def get_all_candidates():
    """
    Fetch all candidates from MongoDB.
    
    Returns:
        List of candidate documents
    """
    candidates = get_db_connection()
    
    # Fetch candidates
    result = []
    for cand in candidates.find():
        result.append(cand)
    
    return result