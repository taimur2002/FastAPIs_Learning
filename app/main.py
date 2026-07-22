from fastapi import FastAPI

from app.database import Base, engine
from app import models  # noqa: F401 — imported so tables get registered
from app.routers import users, auth

# Create any missing tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A Trello-lite task manager, built step by step.",
    version="0.1.0",
)


@app.get("/", tags=["Root"], summary="Health check")
def read_root():
    """Confirms the API is alive."""
    return {"status": "ok", "message": "Task Management API is alive"}


# Plug in feature routers
app.include_router(auth.router)
app.include_router(users.router)
