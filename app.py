from typing import Optional

from fastapi import FastAPI, HTTPException, status, Query, Path
from pydantic import BaseModel

# Create a FastAPI app instance
app = FastAPI(
    title="My Items API",
    description="A learning API for managing items. Built step by step while learning FastAPI.",
    version="0.1.0",
)

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

@app.get("/", tags=["Root"], summary="Health check / welcome message")
def read_root():
    """Simple welcome endpoint — useful for checking that the API is alive."""
    return {"message": "Hello World"}

@app.get(
    "/items/{item_id}",
    tags=["Items"],
    summary="Get a single item by ID",
    response_model=ItemOut,
    response_description="The requested item",
    responses={404: {"description": "Item not found"}},
)
def read_item(
    item_id: int = Path(ge=0, description="The ID of the item to fetch"),
):
    """
    Fetch a single item by its ID.

    - Returns the item if it exists.
    - Returns **404** if no item with that ID is found.
    """
    for item in items:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.get(
    "/items",
    tags=["Items"],
    summary="List items (with pagination and optional search)",
    response_model=list[ItemOut],
    response_description="A list of items matching the filters",
)
def list_items(
    skip: int = Query(default=0, ge=0, description="How many items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        description="Optional search text — filters items whose name contains this",
    ),
):
    """
    List items with pagination and optional name search.

    - **skip**: how many items to skip (for pagination)
    - **limit**: maximum number of items to return (1–100)
    - **q**: optional case-insensitive search by name
    """
    results = items
    if q:
        results = [item for item in results if q.lower() in item["name"].lower()]
    return results[skip : skip + limit]

@app.post(
    "/items",
    tags=["Items"],
    summary="Create a new item",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemOut,
    response_description="The newly created item, including its server-assigned ID",
)
def create_item(item: ItemIn):
    """Create a brand new item. The server assigns the `item_id` automatically."""
    global next_id
    new_item = {"item_id": next_id, **item.model_dump()}
    items.append(new_item)
    next_id += 1
    return new_item

@app.put(
    "/items/{item_id}",
    tags=["Items"],
    summary="Replace an existing item",
    response_model=ItemOut,
    response_description="The updated item",
    responses={404: {"description": "Item not found"}},
)
def update_item(
    item: ItemIn,
    item_id: int = Path(ge=0, description="The ID of the item to update"),
):
    """Replace an existing item entirely. Returns 404 if it doesn't exist."""
    for index, existing in enumerate(items):
        if existing["item_id"] == item_id:
            updated = {"item_id": item_id, **item.model_dump()}
            items[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete(
    "/items/{item_id}",
    tags=["Items"],
    summary="Delete an item",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Item not found"}},
)
def delete_item(
    item_id: int = Path(ge=0, description="The ID of the item to delete"),
):
    """Delete an item by ID. Returns no body on success."""
    for index, existing in enumerate(items):
        if existing["item_id"] == item_id:
            items.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")
