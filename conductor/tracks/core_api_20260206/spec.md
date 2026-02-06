# Track Specification: Core API & Discovery Logic

## Goal
To build the foundational REST API service for a Tinder-like system, focusing on profile management, discovery feed generation with geo-spatial filtering (zones), and mutual match detection logic. This prototype uses an in-memory data store and mock data.

## Core Features
1.  **User Profile Management:**
    -   Create and retrieve user profiles.
    -   Attributes: `user_id`, `name`, `age`, `gender`, `zone_id` (for location).
2.  **Discovery Feed:**
    -   Generate a feed of potential matches.
    -   **Filtering Rules:**
        -   **Location:** Only users in the same `zone_id` as the requester.
        -   **Unseen:** Exclude users already liked or passed by the requester.
        -   **Self:** Exclude the requester themselves.
3.  **Swiping & Matching:**
    -   Record "like" (Right Swipe) or "pass" (Left Swipe) actions.
    -   **Mutual Match Logic:** If User A likes User B, check if User B has already liked User A.
    -   **Response:** If a mutual match occurs, the API response must indicate `is_match: true`.
4.  **Match Listing:**
    -   Retrieve a list of all mutual matches for a user.

## Data Model (In-Memory)
-   **User:**
    -   `id`: UUID
    -   `name`: String
    -   `age`: Integer
    -   `gender`: String
    -   `zone_id`: String (e.g., "NYC", "LDN")
-   **Swipe:**
    -   `swiper_id`: UUID
    -   `swiped_id`: UUID
    -   `action`: Enum ("LIKE", "PASS")
    -   `timestamp`: Datetime
-   **Match:**
    -   `user1_id`: UUID
    -   `user2_id`: UUID
    -   `timestamp`: Datetime

## API Endpoints (Draft)
-   `POST /users/` - Create a user.
-   `GET /users/{user_id}` - Get user details.
-   `GET /feed?user_id={user_id}` - Get discovery feed.
-   `POST /swipe` - Submit a swipe action. Body: `{ swiper_id, swiped_id, action }`. Response: `{ match: boolean }`.
-   `GET /matches?user_id={user_id}` - Get user's matches.

## Non-Functional Requirements
-   **Explainability:** Detailed comments/logs for feed filtering and match detection.
-   **Testability:** High test coverage for `FeedService` and `MatchService`.
-   **Error Handling:** Clear, informative error messages (e.g., "User not found", "Invalid action").
