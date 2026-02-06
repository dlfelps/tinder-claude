"""User management API routes.

Provides endpoints for creating and retrieving user profiles.
"""

import uuid

from fastapi import APIRouter, HTTPException

from app.models.schemas import ApiResponse, User, UserCreateRequest
from app.services.store import get_store

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201)
def create_user(request: UserCreateRequest) -> ApiResponse:
    """Create a new user profile.

    Args:
        request: The user creation payload.

    Returns:
        ApiResponse containing the created user data.
    """
    store = get_store()
    user = User(
        name=request.name,
        age=request.age,
        gender=request.gender,
        zone_id=request.zone_id,
    )
    store.add_user(user)
    return ApiResponse(data=user.model_dump(mode="json"))


@router.get("/{user_id}")
def get_user(user_id: uuid.UUID) -> ApiResponse:
    """Retrieve a user profile by ID.

    Args:
        user_id: The UUID of the user to retrieve.

    Returns:
        ApiResponse containing the user data.

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
    return ApiResponse(data=user.model_dump(mode="json"))
