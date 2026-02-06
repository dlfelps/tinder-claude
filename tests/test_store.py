"""Unit tests for the InMemoryStore."""

import uuid

from app.models.schemas import Match, Swipe, SwipeAction, User
from app.services.store import InMemoryStore, get_store


class TestInMemoryStoreSingleton:
    """Tests for the singleton behavior of InMemoryStore."""

    def test_singleton_returns_same_instance(self):
        """Two calls to InMemoryStore() return the same object."""
        store1 = InMemoryStore()
        store2 = InMemoryStore()
        assert store1 is store2

    def test_get_store_returns_singleton(self):
        """get_store() returns the singleton instance."""
        store = InMemoryStore()
        assert get_store() is store


class TestUserOperations:
    """Tests for user CRUD operations on the store."""

    def test_add_and_get_user(self, reset_store):
        """Adding a user and retrieving by ID returns the same user."""
        store = reset_store
        user = User(name="Test", age=25, gender="male", zone_id="NYC")
        store.add_user(user)
        retrieved = store.get_user(user.id)
        assert retrieved is not None
        assert retrieved.name == "Test"
        assert retrieved.id == user.id

    def test_get_user_not_found(self, reset_store):
        """Getting a non-existent user returns None."""
        store = reset_store
        result = store.get_user(uuid.uuid4())
        assert result is None

    def test_get_all_users(self, reset_store):
        """get_all_users returns all added users."""
        store = reset_store
        u1 = User(name="A", age=20, gender="f", zone_id="NYC")
        u2 = User(name="B", age=21, gender="m", zone_id="LDN")
        store.add_user(u1)
        store.add_user(u2)
        all_users = store.get_all_users()
        assert len(all_users) == 2

    def test_reset_clears_users(self, reset_store):
        """reset() removes all users from the store."""
        store = reset_store
        store.add_user(User(name="X", age=20, gender="f", zone_id="NYC"))
        store.reset()
        assert len(store.get_all_users()) == 0


class TestSwipeOperations:
    """Tests for swipe operations on the store."""

    def test_add_and_get_swipes_by_user(self, reset_store):
        """Swipes are retrievable by swiper_id."""
        store = reset_store
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        swipe = Swipe(
            swiper_id=uid1,
            swiped_id=uid2,
            action=SwipeAction.LIKE,
        )
        store.add_swipe(swipe)
        swipes = store.get_swipes_by_user(uid1)
        assert len(swipes) == 1
        assert swipes[0].swiped_id == uid2

    def test_find_swipe_exists(self, reset_store):
        """find_swipe returns matching swipe when it exists."""
        store = reset_store
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        swipe = Swipe(
            swiper_id=uid1,
            swiped_id=uid2,
            action=SwipeAction.LIKE,
        )
        store.add_swipe(swipe)
        found = store.find_swipe(uid1, uid2)
        assert found is not None
        assert found.action == SwipeAction.LIKE

    def test_find_swipe_not_found(self, reset_store):
        """find_swipe returns None when no matching swipe exists."""
        store = reset_store
        result = store.find_swipe(uuid.uuid4(), uuid.uuid4())
        assert result is None

    def test_reset_clears_swipes(self, reset_store):
        """reset() removes all swipes from the store."""
        store = reset_store
        store.add_swipe(
            Swipe(
                swiper_id=uuid.uuid4(),
                swiped_id=uuid.uuid4(),
                action=SwipeAction.PASS,
            )
        )
        store.reset()
        assert len(store.swipes) == 0


class TestMatchOperations:
    """Tests for match operations on the store."""

    def test_add_and_get_matches(self, reset_store):
        """Matches are retrievable for either user in the pair."""
        store = reset_store
        uid1 = uuid.uuid4()
        uid2 = uuid.uuid4()
        match = Match(user1_id=uid1, user2_id=uid2)
        store.add_match(match)

        matches_for_1 = store.get_matches_for_user(uid1)
        matches_for_2 = store.get_matches_for_user(uid2)
        assert len(matches_for_1) == 1
        assert len(matches_for_2) == 1

    def test_get_matches_empty(self, reset_store):
        """Getting matches for a user with none returns empty list."""
        store = reset_store
        result = store.get_matches_for_user(uuid.uuid4())
        assert result == []

    def test_reset_clears_matches(self, reset_store):
        """reset() removes all matches from the store."""
        store = reset_store
        store.add_match(Match(user1_id=uuid.uuid4(), user2_id=uuid.uuid4()))
        store.reset()
        assert len(store.matches) == 0
