"""Swipe processing and match detection service.

Handles recording swipe actions and detecting mutual matches
when two users have both liked each other.
"""

import uuid

from app.models.schemas import Match, Swipe, SwipeAction
from app.services.store import InMemoryStore


class SwipeService:
    """Processes swipe actions and detects mutual matches.

    When a LIKE swipe is recorded, the service checks whether
    the swiped user has already liked the swiper. If so, a
    Match record is created.
    """

    def __init__(self, store: InMemoryStore) -> None:
        """Initialize SwipeService with a data store.

        Args:
            store: The in-memory data store.
        """
        self.store = store

    def process_swipe(
        self,
        swiper_id: uuid.UUID,
        swiped_id: uuid.UUID,
        action: SwipeAction,
    ) -> bool:
        """Process a swipe action and check for mutual match.

        Records the swipe and, if the action is LIKE, checks
        whether the swiped user has already liked the swiper.
        If a mutual like is found, a Match record is created.

        Args:
            swiper_id: UUID of the user performing the swipe.
            swiped_id: UUID of the user being swiped on.
            action: The swipe action (LIKE or PASS).

        Returns:
            True if a mutual match was detected, False otherwise.

        Raises:
            ValueError: If either user does not exist, or if the
                user tries to swipe on themselves.
        """
        if swiper_id == swiped_id:
            raise ValueError("A user cannot swipe on themselves")

        if self.store.get_user(swiper_id) is None:
            raise ValueError(f"Swiper {swiper_id} not found")

        if self.store.get_user(swiped_id) is None:
            raise ValueError(f"Swiped user {swiped_id} not found")

        # Record the swipe
        swipe = Swipe(
            swiper_id=swiper_id,
            swiped_id=swiped_id,
            action=action,
        )
        self.store.add_swipe(swipe)

        # Check for mutual match only on LIKE
        if action != SwipeAction.LIKE:
            return False

        reverse_swipe = self.store.find_swipe(
            swiper_id=swiped_id, swiped_id=swiper_id
        )

        if reverse_swipe and reverse_swipe.action == SwipeAction.LIKE:
            match = Match(
                user1_id=swiper_id,
                user2_id=swiped_id,
            )
            self.store.add_match(match)
            return True

        return False
