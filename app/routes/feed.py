"""Discovery feed API routes.

Provides the endpoint for generating a user's discovery feed
of potential matches, filtered by zone and seen-state.
"""

import uuid

from fastapi import APIRouter, HTTPException

from app.models.schemas import ApiResponse
from app.services.feed_service import FeedService
from app.services.store import get_store

router = APIRouter(tags=["feed"])


@router.get("/feed")
def get_feed(user_id: uuid.UUID) -> ApiResponse:
    """Generate a discovery feed for the given user.

    Retrieves a list of potential matches filtered by zone,
    self-exclusion, and unseen rules.

    Args:
        user_id: The UUID of the requesting user (query param).

    Returns:
        ApiResponse containing a list of user profiles.

    Raises:
        HTTPException: If the user is not found.
    """
    store = get_store()
    service = FeedService(store)
    try:
        feed = service.generate_feed(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return ApiResponse(
        data=[u.model_dump(mode="json") for u in feed],
        meta={"count": len(feed)},
    )
