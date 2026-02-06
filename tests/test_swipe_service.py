"""Unit tests for SwipeService."""

import uuid

import pytest

from app.models.schemas import SwipeAction
from app.services.swipe_service import SwipeService


class TestSwipeProcessing:
    """Tests for swipe recording and match detection."""

    def test_like_without_mutual_returns_false(self, reset_store, sample_users):
        """A LIKE with no reciprocal like returns is_match=False."""
        store = reset_store
        service = SwipeService(store)
        alice, bob = sample_users[0], sample_users[1]

        result = service.process_swipe(alice.id, bob.id, SwipeAction.LIKE)
        assert result is False

    def test_pass_returns_false(self, reset_store, sample_users):
        """A PASS always returns is_match=False."""
        store = reset_store
        service = SwipeService(store)
        alice, bob = sample_users[0], sample_users[1]

        result = service.process_swipe(alice.id, bob.id, SwipeAction.PASS)
        assert result is False

    def test_mutual_like_creates_match(self, reset_store, sample_users):
        """When both users LIKE each other, a match is created."""
        store = reset_store
        service = SwipeService(store)
        alice, bob = sample_users[0], sample_users[1]

        # Bob likes Alice first (no match yet)
        result1 = service.process_swipe(bob.id, alice.id, SwipeAction.LIKE)
        assert result1 is False

        # Alice likes Bob back (mutual match!)
        result2 = service.process_swipe(alice.id, bob.id, SwipeAction.LIKE)
        assert result2 is True

        # Verify match was recorded
        matches = store.get_matches_for_user(alice.id)
        assert len(matches) == 1
        assert matches[0].user1_id == alice.id
        assert matches[0].user2_id == bob.id

    def test_like_after_pass_no_match(self, reset_store, sample_users):
        """If one user passed, a like from the other is not a match."""
        store = reset_store
        service = SwipeService(store)
        alice, bob = sample_users[0], sample_users[1]

        # Bob passes on Alice
        service.process_swipe(bob.id, alice.id, SwipeAction.PASS)

        # Alice likes Bob (but Bob passed, so no match)
        result = service.process_swipe(alice.id, bob.id, SwipeAction.LIKE)
        assert result is False

    def test_swipe_records_in_store(self, reset_store, sample_users):
        """Swipes are properly recorded in the store."""
        store = reset_store
        service = SwipeService(store)
        alice, bob = sample_users[0], sample_users[1]

        service.process_swipe(alice.id, bob.id, SwipeAction.LIKE)

        swipes = store.get_swipes_by_user(alice.id)
        assert len(swipes) == 1
        assert swipes[0].action == SwipeAction.LIKE

    def test_swipe_self_raises(self, reset_store, sample_users):
        """Swiping on yourself raises a ValueError."""
        store = reset_store
        service = SwipeService(store)
        alice = sample_users[0]

        with pytest.raises(ValueError, match="cannot swipe"):
            service.process_swipe(alice.id, alice.id, SwipeAction.LIKE)

    def test_swipe_nonexistent_swiper_raises(self, reset_store):
        """Swiping from a non-existent user raises ValueError."""
        store = reset_store
        service = SwipeService(store)

        with pytest.raises(ValueError, match="not found"):
            service.process_swipe(uuid.uuid4(), uuid.uuid4(), SwipeAction.LIKE)

    def test_swipe_nonexistent_target_raises(self, reset_store, sample_users):
        """Swiping on a non-existent target raises ValueError."""
        store = reset_store
        service = SwipeService(store)
        alice = sample_users[0]

        with pytest.raises(ValueError, match="not found"):
            service.process_swipe(alice.id, uuid.uuid4(), SwipeAction.LIKE)
