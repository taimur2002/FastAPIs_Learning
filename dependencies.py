from fastapi import HTTPException, Query, Path

import storage


def pagination_params(
    skip: int = Query(default=0, ge=0, description="How many items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
):
    """Shared pagination — inject into any list endpoint."""
    return {"skip": skip, "limit": limit}


def get_item_or_404(
    item_id: int = Path(ge=0, description="The ID of the item"),
):
    """Find an item by ID or raise 404. Returns (index, item)."""
    for index, item in enumerate(storage.items):
        if item["item_id"] == item_id:
            return {"index": index, "item": item}
    raise HTTPException(status_code=404, detail="Item not found")
