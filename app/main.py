"""FastAPI application entry point.

Assembles the Tinder-like backend API by including all route modules.
"""

from fastapi import FastAPI

from app.routes import feed, swipe, users

app = FastAPI(
    title="Tinder-Claude API",
    description=(
        "A Tinder-like backend prototype demonstrating profile "
        "management, discovery feed generation with geo-spatial "
        "filtering, and mutual match detection."
    ),
    version="0.1.0",
)

app.include_router(users.router)
app.include_router(feed.router)
app.include_router(swipe.router)


@app.get("/")
def root() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "tinder-claude"}
