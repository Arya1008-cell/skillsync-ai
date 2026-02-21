import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Force it to load the .env file
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")

# If it can't find the URL, stop immediately!
if not MONGO_URI:
    raise ValueError("🚨 ERROR: MONGODB_URI is empty! Python cannot find your .env file.")

# Set a 5-second timeout so it doesn't hang the frontend forever if it fails
client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client.skillsync_db
assessments_collection = db.assessments

try:
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas Cloud!")
except Exception as e:
    print(f"❌ MongoDB connection error: {e}")