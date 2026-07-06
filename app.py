from fastapi import FastAPI

from routers import items

app = FastAPI(
    title="My Items API",
    description="A learning API for managing items. Built step by step while learning FastAPI.",
    version="0.1.0",
)


@app.get("/", tags=["Root"], summary="Health check / welcome message")
def read_root():
    """Simple welcome endpoint — useful for checking that the API is alive."""
    return {"message": "Hello World"}


# Plug in topic-specific routers
app.include_router(items.router)
