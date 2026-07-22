from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


# The "users" table
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)         # auto ID
    username = Column(String, unique=True, nullable=False, index=True)  # must be unique
    email = Column(String, unique=True, nullable=False, index=True)     # must be unique
    hashed_password = Column(String, nullable=False)                # bcrypt hash (never plain)
    full_name = Column(String, nullable=True)                       # optional
    is_active = Column(Boolean, default=True)                       # default True
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # auto timestamp
