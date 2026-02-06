"""Swipe and match API routes.

Provides endpoints for submitting swipe actions and
retrieving a user's mutual matches.
"""

import uuid

from fastapi import APIRouter, HTTPException

from app.models.schemas import ApiResponse, SwipeRequest
from app.services.store import get_store
from app.services.swipe_service import SwipeService

router = APIRouter(tags=["swipe"])


@router.post("/swipe", status_code=201)
def submit_swipe(request: SwipeRequest) -> ApiResponse:
    """Submit a swipe action (LIKE or PASS).

    Records the swipe and checks for a mutual match.
    If both users have liked each other, is_match is True.

    Args:
        request: The swipe action payload.

    Returns:
        ApiResponse containing the match result.

    Raises:
        HTTPException: If a referenced user is not found or
            the user tries to swipe on themselves.
    """
    store = get_store()
    service = SwipeService(store)
    try:
        is_match = service.process_swipe(
            swiper_id=request.swiper_id,
            swiped_id=request.swiped_id,
            action=request.action,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ApiResponse(data={"is_match": is_match})


@router.get("/matches")
def get_matches(user_id: uuid.UUID) -> ApiResponse:
    """Retrieve all mutual matches for a user.

    Args:
        user_id: The UUID of the user (query param).

    Returns:
        ApiResponse containing a list of match records.

    Raises:
        HTTPException: If the user is not found.
    """
    store = get_store()
    user = store.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found",
        )
    matches = store.get_matches_for_user(user_id)
    return ApiResponse(
        data=[m.model_dump(mode="json") for m in matches],
        meta={"count": len(matches)},
    )
