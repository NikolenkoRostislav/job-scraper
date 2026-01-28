"""
src.api

This package contains the FastAPI application and all API endpoints for IT-JobScraper.

- main.py:
    The entry point for the FastAPI app, including app creation, middleware registration, and route inclusion.

- dependencies.py:
    Shared fastapi dependencies for API endpoints, such as DatabaseDep, CurrentUserDep, AdminDep and JobFilterDep

- exception_handler.py:
    Centralized exception handling for the API, mapping custom and standard exceptions to HTTP responses.

- middleware.py:
    Custom middleware for logging slow responses.

- routes:
    Contains all the route modules, each responsible for a specific feature domain.

"""