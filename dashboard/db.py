
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://ridhinyashrees_db_user:ICPz5lmFNVdkvski@cluster0.k9mo670.mongodb.net/?appName=Cluster0")

# Database
db = client["accident_db"]

# Collection
collection = db["accidents"]
