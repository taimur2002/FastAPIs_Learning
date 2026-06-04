from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create a FastAPI app instance
app = FastAPI()

# Pydantic model for item data
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory storage for items
items = []

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    result = items[item_id].copy()
    if q:
        result["q"] = q
    return result

@app.get("/items")
def list_items():
    return items

@app.post("/items")
def create_item(item: Item):
    new_item = item.dict()
    items.append(new_item)
    return {"item_id": len(items) - 1, **new_item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id] = item.dict()
    return {"item_id": item_id, **items[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    deleted = items.pop(item_id)
    return {"deleted_item_id": item_id, **deleted}
