from fastapi import APIRouter, HTTPException, status, Query, Path

import storage
from models import ItemIn, ItemOut

# A mini-FastAPI for everything under /items
router = APIRouter(prefix="/items", tags=["Items"])


@router.get(
    "/{item_id}",
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
    for item in storage.items:
        if item["item_id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@router.get(
    "/",
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
    results = storage.items
    if q:
        results = [item for item in results if q.lower() in item["name"].lower()]
    return results[skip : skip + limit]


@router.post(
    "/",
    summary="Create a new item",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemOut,
    response_description="The newly created item, including its server-assigned ID",
)
def create_item(item: ItemIn):
    """Create a brand new item. The server assigns the `item_id` automatically."""
    new_item = {"item_id": storage.next_id, **item.model_dump()}
    storage.items.append(new_item)
    storage.next_id += 1
    return new_item


@router.put(
    "/{item_id}",
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
    for index, existing in enumerate(storage.items):
        if existing["item_id"] == item_id:
            updated = {"item_id": item_id, **item.model_dump()}
            storage.items[index] = updated
            return updated
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete(
    "/{item_id}",
    summary="Delete an item",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Item not found"}},
)
def delete_item(
    item_id: int = Path(ge=0, description="The ID of the item to delete"),
):
    """Delete an item by ID. Returns no body on success."""
    for index, existing in enumerate(storage.items):
        if existing["item_id"] == item_id:
            storage.items.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")
