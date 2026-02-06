"""In-memory data store for the application.

Provides a singleton store that holds all users, swipes, and matches
in Python dictionaries for rapid prototyping without database overhead.
"""

import uuid

from app.models.schemas import Match, Swipe, User


class InMemoryStore:
    """Singleton in-memory store for users, swipes, and matches.

    Uses dictionaries for O(1) lookups by ID and efficient
    filtering for feed generation and match detection.
    """

    _instance: "InMemoryStore | None" = None

    def __new__(cls) -> "InMemoryStore":
        """Ensure only one instance of the store exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize store collections if not already done."""
        if self._initialized:
            return
        self._initialized = True
        self.users: dict[uuid.UUID, User] = {}
        self.swipes: list[Swipe] = []
        self.matches: list[Match] = []

    def reset(self) -> None:
        """Clear all data. Useful for testing."""
        self.users.clear()
        self.swipes.clear()
        self.matches.clear()

    # --- User operations ---

    def add_user(self, user: User) -> User:
        """Add a user to the store.

        Args:
            user: The user to add.

        Returns:
            The added user.
        """
        self.users[user.id] = user
        return user

    def get_user(self, user_id: uuid.UUID) -> User | None:
        """Retrieve a user by ID.

        Args:
            user_id: The UUID of the user.

        Returns:
            The user if found, otherwise None.
        """
        return self.users.get(user_id)

    def get_all_users(self) -> list[User]:
        """Retrieve all users.

        Returns:
            A list of all users in the store.
        """
        return list(self.users.values())

    # --- Swipe operations ---

    def add_swipe(self, swipe: Swipe) -> Swipe:
        """Record a swipe action.

        Args:
            swipe: The swipe to record.

        Returns:
            The recorded swipe.
        """
        self.swipes.append(swipe)
        return swipe

    def get_swipes_by_user(self, user_id: uuid.UUID) -> list[Swipe]:
        """Get all swipes made by a specific user.

        Args:
            user_id: The UUID of the swiper.

        Returns:
            A list of swipes made by the user.
        """
        return [s for s in self.swipes if s.swiper_id == user_id]

    def find_swipe(
        self, swiper_id: uuid.UUID, swiped_id: uuid.UUID
    ) -> Swipe | None:
        """Find a specific swipe between two users.

        Args:
            swiper_id: The UUID of the swiper.
            swiped_id: The UUID of the swiped user.

        Returns:
            The swipe if found, otherwise None.
        """
        for swipe in self.swipes:
            if swipe.swiper_id == swiper_id and swipe.swiped_id == swiped_id:
                return swipe
        return None

    # --- Match operations ---

    def add_match(self, match: Match) -> Match:
        """Record a mutual match.

        Args:
            match: The match to record.

        Returns:
            The recorded match.
        """
        self.matches.append(match)
        return match

    def get_matches_for_user(self, user_id: uuid.UUID) -> list[Match]:
        """Get all matches involving a specific user.

        Args:
            user_id: The UUID of the user.

        Returns:
            A list of matches involving the user.
        """
        return [
            m
            for m in self.matches
            if m.user1_id == user_id or m.user2_id == user_id
        ]


def get_store() -> InMemoryStore:
    """Get the singleton store instance.

    Returns:
        The InMemoryStore singleton.
    """
    return InMemoryStore()
