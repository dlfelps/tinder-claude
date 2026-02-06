"""Feed generation service.

Implements the discovery feed algorithm that filters potential
matches based on zone, seen-state, and self-exclusion rules.
"""

import uuid

from app.models.schemas import SwipeAction, User
from app.services.store import InMemoryStore


class FeedService:
    """Generates a discovery feed of potential matches for a user.

    Filtering rules applied in order:
    1. Zone: Only users in the same zone_id as the requester.
    2. Self: Exclude the requester themselves.
    3. Unseen: Exclude users already swiped (liked or passed).
    """

    def __init__(self, store: InMemoryStore) -> None:
        """Initialize FeedService with a data store.

        Args:
            store: The in-memory data store.
        """
        self.store = store

    def generate_feed(self, user_id: uuid.UUID) -> list[User]:
        """Generate a discovery feed for the given user.

        Applies zone filtering, self-exclusion, and unseen
        filtering to produce a list of potential matches.

        Args:
            user_id: The UUID of the requesting user.

        Returns:
            A list of User objects representing potential matches.

        Raises:
            ValueError: If the user_id does not exist.
        """
        requester = self.store.get_user(user_id)
        if requester is None:
            raise ValueError(f"User {user_id} not found")

        # Collect IDs of users already swiped by the requester
        swiped_ids = {
            s.swiped_id
            for s in self.store.get_swipes_by_user(user_id)
            if s.action in (SwipeAction.LIKE, SwipeAction.PASS)
        }

        feed = []
        for user in self.store.get_all_users():
            # Rule 1: Same zone only
            if user.zone_id != requester.zone_id:
                continue
            # Rule 2: Exclude self
            if user.id == user_id:
                continue
            # Rule 3: Exclude already-swiped users
            if user.id in swiped_ids:
                continue
            feed.append(user)

        return feed
