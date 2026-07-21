import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load DATABASE_URL from the .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine = pool of connections to Postgres (echo off now for clean logs)
engine = create_engine(DATABASE_URL)

# Session factory = one "conversation" with the DB per request
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base = parent class for all our table models
Base = declarative_base()


# Dependency: give an endpoint a session, then always close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
