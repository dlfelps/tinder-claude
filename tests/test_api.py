"""Integration tests for the API endpoints."""

import uuid


class TestHealthCheck:
    """Tests for the root health check endpoint."""

    def test_root_returns_ok(self, client):
        """GET / returns service status."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestUserApi:
    """Integration tests for user management endpoints."""

    def test_create_user(self, client):
        """POST /users/ creates a user and returns it."""
        payload = {
            "name": "Alice",
            "age": 25,
            "gender": "female",
            "zone_id": "NYC",
        }
        response = client.post("/users/", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["data"]["name"] == "Alice"
        assert body["data"]["zone_id"] == "NYC"
        assert "id" in body["data"]

    def test_get_user(self, client):
        """GET /users/{id} returns the created user."""
        payload = {
            "name": "Bob",
            "age": 28,
            "gender": "male",
            "zone_id": "NYC",
        }
        create_resp = client.post("/users/", json=payload)
        user_id = create_resp.json()["data"]["id"]

        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["name"] == "Bob"

    def test_get_user_not_found(self, client):
        """GET /users/{id} returns 404 for non-existent user."""
        fake_id = uuid.uuid4()
        response = client.get(f"/users/{fake_id}")
        assert response.status_code == 404

    def test_create_user_invalid_body(self, client):
        """POST /users/ with missing fields returns 422."""
        response = client.post("/users/", json={"name": "X"})
        assert response.status_code == 422


class TestFeedApi:
    """Integration tests for the discovery feed endpoint."""

    def test_feed_returns_same_zone_users(self, client):
        """GET /feed filters by zone and excludes self."""
        # Create users in NYC
        alice = client.post(
            "/users/",
            json={
                "name": "Alice",
                "age": 25,
                "gender": "f",
                "zone_id": "NYC",
            },
        ).json()["data"]
        bob = client.post(
            "/users/",
            json={
                "name": "Bob",
                "age": 28,
                "gender": "m",
                "zone_id": "NYC",
            },
        ).json()["data"]
        # Create user in LDN (should not appear in Alice's feed)
        client.post(
            "/users/",
            json={
                "name": "Diana",
                "age": 27,
                "gender": "f",
                "zone_id": "LDN",
            },
        )

        response = client.get("/feed", params={"user_id": alice["id"]})
        assert response.status_code == 200
        body = response.json()
        feed_ids = [u["id"] for u in body["data"]]

        assert bob["id"] in feed_ids
        assert alice["id"] not in feed_ids
        assert body["meta"]["count"] == 1

    def test_feed_nonexistent_user(self, client):
        """GET /feed for a non-existent user returns 404."""
        response = client.get("/feed", params={"user_id": str(uuid.uuid4())})
        assert response.status_code == 404


class TestSwipeApi:
    """Integration tests for swipe and match endpoints."""

    def _create_user(self, client, name, zone_id="NYC"):
        """Helper to create a user and return the response data."""
        return client.post(
            "/users/",
            json={
                "name": name,
                "age": 25,
                "gender": "other",
                "zone_id": zone_id,
            },
        ).json()["data"]

    def test_swipe_like_no_match(self, client):
        """POST /swipe with a LIKE and no reciprocal returns false."""
        alice = self._create_user(client, "Alice")
        bob = self._create_user(client, "Bob")

        response = client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": bob["id"],
                "action": "LIKE",
            },
        )
        assert response.status_code == 201
        assert response.json()["data"]["is_match"] is False

    def test_swipe_mutual_like_match(self, client):
        """POST /swipe with mutual LIKE returns is_match=True."""
        alice = self._create_user(client, "Alice")
        bob = self._create_user(client, "Bob")

        # Bob likes Alice
        client.post(
            "/swipe",
            json={
                "swiper_id": bob["id"],
                "swiped_id": alice["id"],
                "action": "LIKE",
            },
        )

        # Alice likes Bob back -> match!
        response = client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": bob["id"],
                "action": "LIKE",
            },
        )
        assert response.json()["data"]["is_match"] is True

    def test_swipe_pass_no_match(self, client):
        """POST /swipe with PASS returns is_match=False."""
        alice = self._create_user(client, "Alice")
        bob = self._create_user(client, "Bob")

        response = client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": bob["id"],
                "action": "PASS",
            },
        )
        assert response.json()["data"]["is_match"] is False

    def test_swipe_self_returns_400(self, client):
        """POST /swipe on yourself returns 400."""
        alice = self._create_user(client, "Alice")
        response = client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": alice["id"],
                "action": "LIKE",
            },
        )
        assert response.status_code == 400

    def test_swipe_invalid_action_returns_422(self, client):
        """POST /swipe with invalid action returns 422."""
        alice = self._create_user(client, "Alice")
        bob = self._create_user(client, "Bob")
        response = client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": bob["id"],
                "action": "INVALID",
            },
        )
        assert response.status_code == 422

    def test_get_matches(self, client):
        """GET /matches returns matches for a user."""
        alice = self._create_user(client, "Alice")
        bob = self._create_user(client, "Bob")

        # Create mutual match
        client.post(
            "/swipe",
            json={
                "swiper_id": bob["id"],
                "swiped_id": alice["id"],
                "action": "LIKE",
            },
        )
        client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": bob["id"],
                "action": "LIKE",
            },
        )

        response = client.get("/matches", params={"user_id": alice["id"]})
        assert response.status_code == 200
        body = response.json()
        assert body["meta"]["count"] == 1

    def test_get_matches_empty(self, client):
        """GET /matches for user with no matches returns empty."""
        alice = self._create_user(client, "Alice")
        response = client.get("/matches", params={"user_id": alice["id"]})
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_get_matches_nonexistent_user(self, client):
        """GET /matches for non-existent user returns 404."""
        response = client.get(
            "/matches",
            params={"user_id": str(uuid.uuid4())},
        )
        assert response.status_code == 404

    def test_feed_excludes_swiped_users(self, client):
        """Feed excludes users that have been swiped on."""
        alice = self._create_user(client, "Alice")
        bob = self._create_user(client, "Bob")
        charlie = self._create_user(client, "Charlie")

        # Alice likes Bob
        client.post(
            "/swipe",
            json={
                "swiper_id": alice["id"],
                "swiped_id": bob["id"],
                "action": "LIKE",
            },
        )

        # Feed should no longer contain Bob
        response = client.get("/feed", params={"user_id": alice["id"]})
        feed_ids = [u["id"] for u in response.json()["data"]]
        assert bob["id"] not in feed_ids
        assert charlie["id"] in feed_ids
