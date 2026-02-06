# Product Guidelines

## Communication Style
- **Educational and Explanatory:** Documentation and code comments should prioritize clarity and explain the rationale behind design choices, particularly for complex logic like feed generation and matching algorithms. The goal is to make the system's inner workings accessible and understandable.

## API Design Principles
- **Resource-Oriented REST:** The API must adhere to standard RESTful conventions. Use nouns for resources and appropriate HTTP verbs (GET, POST, PUT, DELETE) for actions.
- **Consistency:** Ensure a uniform experience across all endpoints.
- **Naming Convention:** Use `snake_case` for all API endpoints, request/response fields, and data model attributes (e.g., `user_id`, `discovery_feed`, `match_timestamp`).

## API Response & Error Handling
- **Standardized Envelope:** All API responses must be wrapped in a consistent object structure:
  ```json
  {
    "data": { ... },
    "meta": { ... },
    "errors": [ ... ]
  }
  ```
- **Informative Error Messages:** In the event of a failure, provide a descriptive, human-readable message that explains the cause of the error. Include relevant HTTP status codes and, where helpful, suggestions for resolution.

## Data Modeling
- **Clarity:** Prioritize descriptive field names over brevity to ensure the data model is self-documenting.
- **Separation of Concerns:** Maintain a clear distinction between internal data structures and the public API representations.
