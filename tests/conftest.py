"""Shared test fixtures for the Tinder-Claude test suite."""

import uuid

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import User
from app.services.store import InMemoryStore


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the in-memory store before each test."""
    store = InMemoryStore()
    store.reset()
    yield store
    store.reset()


@pytest.fixture()
def client():
    """Provide a FastAPI test client."""
    return TestClient(app)


@pytest.fixture()
def sample_users(reset_store):
    """Create a set of sample users across two zones."""
    store = reset_store
    users = [
        User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
            name="Alice",
            age=25,
            gender="female",
            zone_id="NYC",
        ),
        User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000002"),
            name="Bob",
            age=28,
            gender="male",
            zone_id="NYC",
        ),
        User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000003"),
            name="Charlie",
            age=30,
            gender="male",
            zone_id="NYC",
        ),
        User(
            id=uuid.UUID("00000000-0000-0000-0000-000000000004"),
            name="Diana",
            age=27,
            gender="female",
            zone_id="LDN",
        ),
    ]
    for user in users:
        store.add_user(user)
    return users
