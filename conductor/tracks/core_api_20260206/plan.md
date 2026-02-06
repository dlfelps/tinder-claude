# Implementation Plan - Core API & Discovery Logic

## Phase 1: Project Skeleton & Data Models
Establish the FastAPI project structure and defining the Pydantic models for the in-memory store.
- [ ] Task: Initialize FastAPI project structure with `app/main.py` and `app/models/`.
- [ ] Task: Create Pydantic models for `User`, `Swipe`, and `Match` in `app/models/schemas.py`.
- [ ] Task: Implement a singleton `InMemoryStore` class to hold lists/dicts of users and swipes.
- [ ] Task: Write unit tests for the `InMemoryStore` basic operations (add/get).
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Project Skeleton & Data Models' (Protocol in workflow.md)

## Phase 2: User Management & Profile API
Implement the ability to create and retrieve users, which is the foundation for everything else.
- [ ] Task: Implement `POST /users/` endpoint to create a new user and save to store.
- [ ] Task: Implement `GET /users/{user_id}` endpoint to retrieve user details.
- [ ] Task: Write integration tests for User API endpoints (create and retrieve).
- [ ] Task: Conductor - User Manual Verification 'Phase 2: User Management & Profile API' (Protocol in workflow.md)

## Phase 3: Discovery Feed Logic
Implement the core algorithm for generating the feed based on location and seen-state.
- [ ] Task: Implement `FeedService.generate_feed(user_id)` logic.
    - [ ] Sub-task: Filter users by matching `zone_id`.
    - [ ] Sub-task: Filter out users already present in `swipes` for the requester.
    - [ ] Sub-task: Filter out the requester themselves.
- [ ] Task: Implement `GET /feed` API endpoint utilizing the `FeedService`.
- [ ] Task: Write unit tests for `FeedService` covering all filtering rules (zone, unseen, self).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Discovery Feed Logic' (Protocol in workflow.md)

## Phase 4: Swiping & Match Detection
Implement the action of swiping and the immediate calculation of matches.
- [ ] Task: Implement `SwipeService.process_swipe(swiper_id, swiped_id, action)` logic.
    - [ ] Sub-task: Record the swipe in the store.
    - [ ] Sub-task: If action is LIKE, check if `swiped_id` has already LIKED `swiper_id`.
    - [ ] Sub-task: If mutual like, create a `Match` record and return `is_match=True`.
- [ ] Task: Implement `POST /swipe` API endpoint.
- [ ] Task: Implement `GET /matches` API endpoint to list matches for a user.
- [ ] Task: Write comprehensive tests for swiping flow, including mutual match scenarios and non-match scenarios.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Swiping & Match Detection' (Protocol in workflow.md)
