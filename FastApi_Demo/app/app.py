from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    
class ItemInDB(Item):
    id: int


app = FastAPI()


items_db: List[ItemInDB] = [
    ItemInDB(id=1, name="Laptop Pro", description="High-end professional notebook.", price=2500.00, tax=250.00),
    ItemInDB(id=2, name="Mechanical Keyboard", description="Clicky tactile switches.", price=150.00, tax=15.00),
    ItemInDB(id=3, name="4K Monitor", description="Large screen with high refresh rate.", price=600.00, tax=60.00),
    ItemInDB(id=4, name="Wireless Mouse", description="Ergonomic design for long use.", price=75.00, tax=7.50),
    ItemInDB(id=5, name="Webcam HD", description="1080p for video calls.", price=50.00, tax=5.00),
    ItemInDB(id=6, name="Noise Cancelling Headphones", description="Premium sound quality and comfort.", price=350.00, tax=35.00),
]
current_id = 7 


@app.get("/", response_model=dict)
def read_root():
    return {"message": "Welcome to the FastAPI Data Service"}

# GET All Items
@app.get("/items/", response_model=List[ItemInDB])
def read_items():
    return items_db

# GET Single Item by ID (Path Parameter)
@app.get("/items/{item_id}", response_model=ItemInDB)
def read_item(item_id: int):
    item = next((item for item in items_db if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# POST (Create) a New Item
@app.post("/items/", response_model=ItemInDB, status_code=201)
def create_item(item: Item):
    global current_id
    new_item = ItemInDB(id=current_id, **item.model_dump())
    items_db.append(new_item)
    current_id += 1
    return new_item

# DELETE an Item by ID
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    global items_db
    initial_length = len(items_db)
    items_db = [item for item in items_db if item.id != item_id]
    
    if len(items_db) == initial_length:
        raise HTTPException(status_code=404, detail="Item not found")
    
   
    return