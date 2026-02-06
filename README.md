# Tinder-Claude

A Tinder-like backend API prototype built with FastAPI. Implements profile management, zone-based discovery feeds, swiping, and mutual match detection using in-memory storage.

## Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd tinder-claude

# Install dependencies with uv (recommended)
uv sync

# Or with pip
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running the Server

```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. Interactive API docs are served at `http://localhost:8000/docs`.

## API Endpoints

### Health Check

```
GET /
```

Returns service status.

### Users

```
POST /users/          # Create a new user
GET  /users/{user_id} # Get a user by ID
```

**Create user request body:**

```json
{
  "name": "Alice",
  "age": 25,
  "gender": "female",
  "zone_id": "zone-1"
}
```

### Discovery Feed

```
GET /feed?user_id={uuid}
```

Returns a list of candidate profiles for the given user. The feed applies three filters:

1. **Zone filtering** -- only users in the same `zone_id`
2. **Self-exclusion** -- the requesting user is never included
3. **Seen-state filtering** -- users already swiped on (like or pass) are excluded

### Swiping

```
POST /swipe
```

**Request body:**

```json
{
  "swiper_id": "uuid",
  "swiped_id": "uuid",
  "action": "LIKE"
}
```

`action` accepts `LIKE` or `PASS`. Returns `{ "is_match": true }` when both users have liked each other.

### Matches

```
GET /matches?user_id={uuid}
```

Returns all matches for the given user.

## Running Tests

```bash
# Run the full test suite
uv run pytest

# Run with coverage
uv run pytest --cov=app --cov-report=html
```

## Linting

```bash
uv run ruff check app/ tests/
uv run ruff format app/ tests/
```

## Project Structure

```
app/
  main.py              # FastAPI application entry point
  models/
    schemas.py         # Pydantic data models (User, Swipe, Match)
  services/
    store.py           # In-memory data store (singleton)
    feed_service.py    # Discovery feed generation
    swipe_service.py   # Swipe recording and match detection
  routes/
    users.py           # User management endpoints
    feed.py            # Feed endpoint
    swipe.py           # Swipe and match endpoints
tests/
  conftest.py          # Shared fixtures
  test_api.py          # Integration tests
  test_store.py        # Store unit tests
  test_feed_service.py # Feed service unit tests
  test_swipe_service.py# Swipe service unit tests
```

## Design Notes

- **In-memory storage** -- all data lives in Python dictionaries via a singleton `InMemoryStore`. Data resets on server restart.
- **Zone-based discovery** -- users are grouped by `zone_id` to simulate geographic proximity.
- **Mutual match detection** -- when a LIKE is recorded, the service checks for a reciprocal LIKE and creates a `Match` record if found.
- **Standardized responses** -- all endpoints return an `ApiResponse` envelope with `data`, `meta`, and `errors` fields.
