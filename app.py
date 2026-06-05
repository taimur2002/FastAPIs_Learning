from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Create a FastAPI app instance
app = FastAPI()

# Pydantic model for data coming IN (from the client)
class ItemIn(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Pydantic model for data going OUT (to the client)
class ItemOut(BaseModel):
    item_id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory storage: each item is a dict that already includes item_id
items = []
next_id = 0  # simple counter so ids don't break when we delete

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}", response_model=ItemOut)
def read_item(item_id: int):
    for item in items:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items", response_model=list[ItemOut])
def list_items():
    return items

@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ItemOut)
def create_item(item: ItemIn):
    global next_id
    new_item = {"item_id": next_id, **item.model_dump()}
    items.append(new_item)
    next_id += 1
    return new_item

@app.put("/items/{item_id}", response_model=ItemOut)
def update_item(item_id: int, item: ItemIn):
    for index, existing in enumerate(items):
        if existing["item_id"] == item_id:
            updated = {"item_id": item_id, **item.model_dump()}
            items[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    for index, existing in enumerate(items):
        if existing["item_id"] == item_id:
            items.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")
