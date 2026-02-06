# Technology Stack

## Core Development
- **Programming Language:** Python 3.10+ (Selected for its readability and suitability for prototyping logic).
- **Web Framework:** FastAPI (Chosen for its high performance, standard-based REST design, and automatic OpenAPI documentation).
- **Data Validation & Modeling:** Pydantic (Used to define robust, typed data structures for the in-memory store and API schemas).

## Data Storage (Prototyping)
- **Persistence:** In-Memory (Using Python dictionaries and Pydantic models for rapid iteration without database overhead).
- **State Management:** Simple singleton or dependency-injected store to manage users, swipes, and matches during the application lifecycle.

## Testing & Quality
- **Test Framework:** pytest (The standard for Python testing, used for unit and integration tests of the API and core algorithms).
- **Linting & Formatting:** ruff (Fast, comprehensive linting and formatting to maintain code quality).

## Environment & Dependencies
- **Package Manager:** uv (An extremely fast Python package installer and resolver).
- **Environment Management:** Managed via `uv` or standard Python virtual environments (`venv`).
