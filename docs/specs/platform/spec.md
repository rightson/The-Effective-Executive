# Capability: platform

## Purpose
Run a local-first web service that exposes the five Drucker modules over HTTP and serves a single-page UI.

## Requirements

### Requirement: Single-process FastAPI app
The service SHALL be a single Python process started via `python3 main.py`, listening on `0.0.0.0:8000`.

#### Scenario: Start
- **WHEN** the user runs `python3 main.py`
- **THEN** uvicorn binds port 8000 and serves both `/api/*` and `/`.

### Requirement: SQLite persistence
The service SHALL persist all data in `effective_executive.db` (SQLite) in the working directory using SQLAlchemy 2.x.

#### Scenario: Schema
- **WHEN** the process starts
- **THEN** `Base.metadata.create_all` creates any missing tables.

#### Scenario: No migrations
- **WHEN** a model field changes incompatibly
- **THEN** the operator must delete the database file; no migration tool ships with the service.

### Requirement: Single user, no auth
The service SHALL NOT authenticate requests. All data is owned by the local operator.

### Requirement: SPA delivery
The service SHALL serve `static/index.html` at `/` and mount `static/` at `/static`.

### Requirement: OpenAPI
The service SHALL expose interactive docs at `/docs` (FastAPI default).
