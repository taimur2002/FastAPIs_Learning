from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# Data coming IN — what the client must send to create a user
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50, examples=["taimur"])
    email: EmailStr                                    # must be a valid email
    password: str = Field(min_length=8, examples=["secret123"])  # plain, gets hashed
    full_name: str | None = Field(default=None, max_length=100)


# Data going OUT — what the API sends back (note: no password ever)
class UserOut(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    created_at: datetime

    # lets Pydantic read straight from a SQLAlchemy row object
    model_config = {"from_attributes": True}


# What the login endpoint returns
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
