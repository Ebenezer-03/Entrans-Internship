# todoapp/mongo_user_service.py
"""User management using MongoDB collection 'users'."""

from typing import Optional, Dict
from pymongo.collection import Collection
from .mongo_client import get_client
from .password_utils import hash_password, verify_password
from bson import ObjectId
import os

DB_NAME = os.getenv("MONGO_DB", "todo_db")
_USERS_COLL = "users"

def _get_users_collection() -> Collection:
    client = get_client()
    db = client[DB_NAME]
    return db[_USERS_COLL]

def create_user(email: str, password: str, full_name: str = "") -> Dict:
    """Create a new user; raises if email exists."""
    coll = _get_users_collection()
    if coll.find_one({"email": email.lower()}):
        raise ValueError("Email already registered")
    hashed = hash_password(password)
    doc = {"email": email.lower(), "password": hashed, "full_name": full_name}
    res = coll.insert_one(doc)
    doc["_id"] = res.inserted_id
    return {"id": str(doc["_id"]), "email": doc["email"], "full_name": doc["full_name"]}

def find_user_by_email(email: str) -> Optional[Dict]:
    coll = _get_users_collection()
    doc = coll.find_one({"email": email.lower()})
    if not doc:
        return None
    return {"id": str(doc["_id"]), "email": doc["email"], "full_name": doc.get("full_name", ""), "password": doc.get("password")}

def verify_user_credentials(email: str, password: str) -> Optional[Dict]:
    user = find_user_by_email(email)
    if not user:
        return None
    stored = user.get("password")
    if not stored:
        return None
    if verify_password(password, stored):
        # return public user (without password)
        return {"id": user["id"], "email": user["email"], "full_name": user.get("full_name", "")}
    return None

def find_user_by_id(user_id: str) -> Optional[Dict]:
    coll = _get_users_collection()
    try:
        doc = coll.find_one({"_id": ObjectId(user_id)})
    except Exception:
        return None
    if not doc:
        return None
    return {"id": str(doc["_id"]), "email": doc["email"], "full_name": doc.get("full_name", "")}
