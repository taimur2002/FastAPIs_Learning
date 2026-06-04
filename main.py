from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create a FastAPI app instance
# This is like the main object that handles all our API routes
app = FastAPI()

# Pydantic model for a request body when creating or updating an item
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# In-memory list to store items while the server is running
items = []

# Define a route to check the server status
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Another route to get an item by ID
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    # item_id is a path parameter (from URL)
    # q is a query parameter (optional, from ?q=something)
    return {"item_id": item_id, "q": q}