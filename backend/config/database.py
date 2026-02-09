from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

# Add tls options for Atlas connection
client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())
db = client["hrms_db"]

# collections
employees_collection = db["employees"]
attendance_collection = db["attendance"]
