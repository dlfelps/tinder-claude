"""Pydantic models for the Tinder-like API.

Defines the data structures for Users, Swipes, and Matches,
as well as the request/response schemas for the API.
"""

import enum
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class SwipeAction(str, enum.Enum):
    """Enum for swipe actions."""

    LIKE = "LIKE"
    PASS = "PASS"


# --- Core Data Models ---


class User(BaseModel):
    """Represents a user profile in the system."""

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str
    age: int
    gender: str
    zone_id: str


class Swipe(BaseModel):
    """Represents a swipe action from one user to another."""

    swiper_id: uuid.UUID
    swiped_id: uuid.UUID
    action: SwipeAction
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class Match(BaseModel):
    """Represents a mutual match between two users."""

    user1_id: uuid.UUID
    user2_id: uuid.UUID
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


# --- API Request Schemas ---


class UserCreateRequest(BaseModel):
    """Request body for creating a new user."""

    name: str
    age: int
    gender: str
    zone_id: str


class SwipeRequest(BaseModel):
    """Request body for submitting a swipe."""

    swiper_id: uuid.UUID
    swiped_id: uuid.UUID
    action: SwipeAction


# --- API Response Schemas ---


class ApiResponse(BaseModel):
    """Standardized API response envelope.

    All API responses are wrapped in this structure
    for consistency, as defined in product-guidelines.md.
    """

    data: Any = None
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[dict[str, Any]] = Field(default_factory=list)


class SwipeResponse(BaseModel):
    """Response body for a swipe action."""

    is_match: bool
