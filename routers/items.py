from fastapi import APIRouter, Depends, Query, status

import storage
from dependencies import get_item_or_404, pagination_params
from models import ItemIn, ItemOut

router = APIRouter(prefix="/items", tags=["Items"])


@router.get(
    "/{item_id}",
    summary="Get a single item by ID",
    response_model=ItemOut,
    responses={404: {"description": "Item not found"}},
)
def read_item(found=Depends(get_item_or_404)):
    """Fetch a single item by ID. Returns 404 if it doesn't exist."""
    return found["item"]


@router.get(
    "/",
    summary="List items (with pagination and optional search)",
    response_model=list[ItemOut],
)
def list_items(
    page: dict = Depends(pagination_params),
    q: str | None = Query(
        default=None,
        min_length=3,
        max_length=50,
        description="Optional case-insensitive search by name",
    ),
):
    """List items with shared pagination and optional name search."""
    results = storage.items
    if q:
        results = [item for item in results if q.lower() in item["name"].lower()]
    return results[page["skip"] : page["skip"] + page["limit"]]


@router.post(
    "/",
    summary="Create a new item",
    status_code=status.HTTP_201_CREATED,
    response_model=ItemOut,
)
def create_item(item: ItemIn):
    """Create a new item. Server assigns the `item_id`."""
    new_item = {"item_id": storage.next_id, **item.model_dump()}
    storage.items.append(new_item)
    storage.next_id += 1
    return new_item


@router.put(
    "/{item_id}",
    summary="Replace an existing item",
    response_model=ItemOut,
    responses={404: {"description": "Item not found"}},
)
def update_item(item: ItemIn, found=Depends(get_item_or_404)):
    """Replace an existing item entirely."""
    updated = {"item_id": found["item"]["item_id"], **item.model_dump()}
    storage.items[found["index"]] = updated
    return updated


@router.delete(
    "/{item_id}",
    summary="Delete an item",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"description": "Item not found"}},
)
def delete_item(found=Depends(get_item_or_404)):
    """Delete an item by ID."""
    storage.items.pop(found["index"])
