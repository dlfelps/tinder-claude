"""Unit tests for FeedService."""

import uuid

import pytest

from app.models.schemas import Swipe, SwipeAction
from app.services.feed_service import FeedService


class TestFeedServiceFiltering:
    """Tests for discovery feed generation and filtering rules."""

    def test_feed_returns_same_zone_users(self, reset_store, sample_users):
        """Feed only contains users in the same zone."""
        store = reset_store
        service = FeedService(store)
        alice = sample_users[0]  # NYC

        feed = service.generate_feed(alice.id)
        feed_ids = {u.id for u in feed}

        # Bob and Charlie are in NYC, Diana is in LDN
        assert sample_users[1].id in feed_ids  # Bob
        assert sample_users[2].id in feed_ids  # Charlie
        assert sample_users[3].id not in feed_ids  # Diana

    def test_feed_excludes_self(self, reset_store, sample_users):
        """Feed does not contain the requesting user."""
        store = reset_store
        service = FeedService(store)
        alice = sample_users[0]

        feed = service.generate_feed(alice.id)
        feed_ids = {u.id for u in feed}

        assert alice.id not in feed_ids

    def test_feed_excludes_liked_users(self, reset_store, sample_users):
        """Feed excludes users the requester has already liked."""
        store = reset_store
        service = FeedService(store)
        alice = sample_users[0]
        bob = sample_users[1]

        # Alice likes Bob
        store.add_swipe(
            Swipe(
                swiper_id=alice.id,
                swiped_id=bob.id,
                action=SwipeAction.LIKE,
            )
        )

        feed = service.generate_feed(alice.id)
        feed_ids = {u.id for u in feed}

        assert bob.id not in feed_ids
        # Charlie should still be in feed
        assert sample_users[2].id in feed_ids

    def test_feed_excludes_passed_users(self, reset_store, sample_users):
        """Feed excludes users the requester has already passed."""
        store = reset_store
        service = FeedService(store)
        alice = sample_users[0]
        bob = sample_users[1]

        # Alice passes on Bob
        store.add_swipe(
            Swipe(
                swiper_id=alice.id,
                swiped_id=bob.id,
                action=SwipeAction.PASS,
            )
        )

        feed = service.generate_feed(alice.id)
        feed_ids = {u.id for u in feed}

        assert bob.id not in feed_ids

    def test_feed_empty_when_all_swiped(self, reset_store, sample_users):
        """Feed is empty when the user has swiped everyone in zone."""
        store = reset_store
        service = FeedService(store)
        alice = sample_users[0]

        # Swipe on all NYC users
        for user in sample_users[1:3]:  # Bob, Charlie
            store.add_swipe(
                Swipe(
                    swiper_id=alice.id,
                    swiped_id=user.id,
                    action=SwipeAction.LIKE,
                )
            )

        feed = service.generate_feed(alice.id)
        assert len(feed) == 0

    def test_feed_for_nonexistent_user_raises(self, reset_store):
        """Generating feed for a non-existent user raises ValueError."""
        store = reset_store
        service = FeedService(store)

        with pytest.raises(ValueError, match="not found"):
            service.generate_feed(uuid.uuid4())

    def test_feed_for_user_in_empty_zone(self, reset_store):
        """Feed for a user alone in their zone is empty."""
        store = reset_store
        service = FeedService(store)
        from app.models.schemas import User

        loner = User(name="Loner", age=30, gender="other", zone_id="EMPTY")
        store.add_user(loner)

        feed = service.generate_feed(loner.id)
        assert len(feed) == 0
