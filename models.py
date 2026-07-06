from typing import Optional

from pydantic import BaseModel


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
