from typing import Dict, List, Optional, Any
from pymongo.collection import Collection
from bson import ObjectId
from .mongo_client import get_collection

def serialize_doc(doc: Dict) -> Dict:
    return {
        "id": str(doc["_id"]),
        "title": doc.get("title", ""),
        "description": doc.get("description", ""),
        "due_date": doc.get("due_date", ""),
        "priority": doc.get("priority", "Low"),
        "progress": int(doc.get("progress", 0)),
        "deleted": bool(doc.get("deleted", False)),
        "archived": bool(doc.get("archived", False)),
        "completed": bool(doc.get("completed", False)),
    }

def list_todos(collection: Collection = None) -> List[Dict]:
    coll = collection or get_collection()
    docs = coll.find().sort("_id", -1)
    return [serialize_doc(d) for d in docs]

def create_todo(data: Dict, collection: Collection = None) -> Dict:
    coll = collection or get_collection()
    result = coll.insert_one(data)
    data["_id"] = result.inserted_id
    return serialize_doc(data)

def patch_todo(todo_id: str, patch_data: Dict, collection: Collection = None) -> Optional[Dict]:
    coll = collection or get_collection()
    try:
        oid = ObjectId(todo_id)
    except Exception:
        return None

    updated = coll.find_one_and_update(
        {"_id": oid},
        {"$set": patch_data},
        return_document=True
    )
    return serialize_doc(updated) if updated else None

def delete_todo(todo_id: str, collection: Collection = None) -> bool:
    coll = collection or get_collection()
    try:
        oid = ObjectId(todo_id)
    except Exception:
        return False

    result = coll.delete_one({"_id": oid})
    return result.deleted_count == 1
