from pymongo import MongoClient
from bson import ObjectId

client = MongoClient("mongodb://localhost:27017")
# Your own databse
db = client["mydb"] 
# Your own collection
users_collection = db["users"]

def get_user_by_email(email: str):
    return users_collection.find_one({"email": email})

def get_user_by_id(user_id: str):
    return users_collection.find_one({"_id": ObjectId(user_id)})
