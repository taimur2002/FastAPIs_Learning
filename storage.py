# Fake in-memory "database" — shared across all routers via module import.
# Replace with a real database in a future lesson.

items: list[dict] = []
next_id: int = 0
