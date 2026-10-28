# NearMates

**NearMates** is a backend application designed to help people who relocate to a new city discover potential friends from a similar regional or linguistic background and with shared interests.

The project is being built incrementally as a hands-on backend engineering learning project, with an emphasis on clean API design, relational data modeling, authentication, automated testing, and performance.

> **Project status:** Core API features and an initial automated test suite are implemented. Redis caching and deployment improvements are planned next. Update this README as new features are completed.

## Table of Contents

- [Problem Statement](#problem-statement)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Design](#database-design)
- [Matching Algorithm](#matching-algorithm)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Security Notes](#security-notes)

## Problem Statement

Relocating for work or education can make it difficult to build a social circle. NearMates aims to help people discover others in their current city who share languages, interests, or a regional background.

For example, someone who moves from Maharashtra to Chennai could use NearMates to discover people nearby who speak Marathi and enjoy activities such as cricket, trekking, gaming, or photography.

## Features

### Implemented

- User registration with request validation.
- Password-based login and JWT bearer authentication.
- Protected endpoints for the authenticated user.
- PostgreSQL persistence using SQLAlchemy.
- Database schema migrations with Alembic.
- Shared language and interest catalogues.
- Authenticated language and interest preference management.
- Discovery endpoint that recommends users in the same current city.
- Rule-based compatibility scoring using shared languages, interests, and home region.
- Pagination for discovery results.
- Automated API and service tests with Pytest.

### Planned

- Redis caching for frequently requested discovery results.
- Cache invalidation when profile or preference changes affect recommendations.
- More efficient database-side filtering, scoring, and pagination.
- Docker Compose configuration for the API, PostgreSQL, and Redis.
- Continuous integration with GitHub Actions.
- Structured logging, monitoring, and deployment.
- Additional profile and connection-request features.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application language |
| FastAPI | HTTP API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database queries |
| Alembic | Database migrations |
| Pydantic | Request validation and response schemas |
| JWT bearer authentication | API authentication |
| Pytest | Automated testing |
| HTTPX | HTTP client used by API tests |
| Redis | Planned caching layer |

## Architecture

The application follows a layered structure:

```text
Client
  |
  v
FastAPI routers
  |
  +--> Authentication and dependencies
  |
  +--> Pydantic request/response schemas
  |
  v
Service layer
  |
  v
SQLAlchemy models and queries
  |
  v
PostgreSQL
```

Redis is planned as a cache for suitable read-heavy operations, especially discovery. PostgreSQL remains the source of truth.

## Project Structure

The structure below is representative. Keep it aligned with the actual files in the repository as the project evolves.

```text
NearMates/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── auth.py
│   ├── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── language.py
│   │   ├── interest.py
│   │   └── associations.py
│   ├── schemas/
│   │   ├── catalogue.py
│   │   └── discovery.py
│   ├── routers/
│   │   ├── catalogue.py
│   │   ├── preferences.py
│   │   └── discovery.py
│   └── services/
│       ├── catalogue.py
│       └── discovery.py
├── migrations/
│   └── versions/
├── tests/
├── alembic.ini
├── requirements.txt
├── seed_catalogue.py
└── README.md
```

Some files may differ in the current implementation. The README should reflect the actual repository rather than introducing files that do not exist.

## Getting Started

### Prerequisites

Install the following:

- Python compatible with the dependencies in `requirements.txt`.
- PostgreSQL.
- Git.
- A terminal such as PowerShell on Windows.

Redis is not required until the Redis caching milestone is implemented.

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd NearMates
```

Replace `<your-repository-url>` with your repository URL.

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, follow your organization's security guidance or activate the environment using a terminal configured for your system.

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

If the project is still under development and the requirements file is incomplete, install the missing development dependencies explicitly:

```powershell
python -m pip install fastapi uvicorn sqlalchemy alembic psycopg pytest httpx
```

Install any additional packages required by the current authentication and configuration implementation.

### 4. Create a PostgreSQL database

Create a development database, for example:

```sql
CREATE DATABASE nearmates_db;
```

Use a PostgreSQL role that has the required permissions. Do not put real database credentials in source code.

### 5. Configure environment variables

Create a local `.env` file in the project root. Adapt the values to match the names expected by `app/config.py`.

Example:

```dotenv
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/nearmates_db
SECRET_KEY=REPLACE_WITH_A_LONG_RANDOM_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace the example values with your local configuration. Never commit `.env` or real secrets to version control.

### 6. Apply database migrations

After confirming that Alembic is configured to use your development database, run:

```powershell
alembic upgrade head
```

Review migration files before applying them, especially when working with a database that already contains data.

### 7. Seed the catalogue

If the catalogue seeding script is present and configured for your development database, run:

```powershell
python seed_catalogue.py
```

This inserts the initial languages and interests used by preference endpoints.

## Running the Application

Start the development server from the project root:

```powershell
uvicorn app.main:app --reload
```

Open the interactive API documentation at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Use the authentication endpoint to obtain a token, then authorize protected requests with a bearer token.

## API Endpoints

The following endpoints are part of the current design. Verify route names against `app/main.py` and the router modules if they change.

| Method | Endpoint | Authentication | Purpose |
|---|---|---|---|
| `GET` | `/health` | Public | Health check |
| `POST` | `/users` | Public | Register a user |
| `POST` | `/auth/login` | Public | Log in and obtain an access token |
| `GET` | `/users/me` | Required | Retrieve the authenticated user's profile |
| `GET` | `/languages` | Public | List available languages |
| `GET` | `/interests` | Public | List available interests |
| `PUT` | `/users/me/languages` | Required | Replace the user's language selection |
| `GET` | `/users/me/languages` | Required | Retrieve the user's language selection |
| `PUT` | `/users/me/interests` | Required | Replace the user's interest selection |
| `GET` | `/users/me/interests` | Required | Retrieve the user's interest selection |
| `GET` | `/discover` | Required | Discover potential connections |

### Example: Update languages

Send a bearer token and a JSON body containing IDs returned by `GET /languages`:

```http
PUT /users/me/languages
Authorization: Bearer <access-token>
Content-Type: application/json
```

```json
{
  "ids": [1, 2]
}
```

The IDs above are examples. Use IDs returned by your running API.

### Example: Discover people

```http
GET /discover?page=1&page_size=10
Authorization: Bearer <access-token>
```

The discovery response includes pagination metadata and candidate details such as shared languages, shared interests, and a match score. It should not expose password hashes or other private authentication data.

## Database Design

The core relational model includes:

- `users`: user account and profile data.
- `languages`: shared language catalogue.
- `interests`: shared interest catalogue.
- `user_languages`: many-to-many association between users and languages.
- `user_interests`: many-to-many association between users and interests.
- `alembic_version`: tracks the applied Alembic migration revision.

The association tables use foreign keys and composite primary keys to prevent duplicate user-to-language or user-to-interest relationships.

Alembic is used to version schema changes. Review generated migrations before applying them.

## Matching Algorithm

The initial discovery algorithm ranks users in the same current city using three signals:

| Signal | Maximum points |
|---|---:|
| Shared languages | 40 |
| Shared interests | 40 |
| Same home region | 20 |
| **Total** | **100** |

Language and interest scores are proportional to the number of preferences the requesting user has selected:

```text
language_score = 40 * shared_languages / user's_language_count
interest_score = 40 * shared_interests / user's_interest_count
regional_score = 20 if home regions match, otherwise 0

match_score = language_score + interest_score + regional_score
```

If the user has no languages or interests selected, that category contributes zero points. Scores are rounded to two decimal places.

This is a transparent, rule-based ranking heuristic—not a prediction of whether two people will become friends. The initial implementation calculates scores in Python and paginates the resulting list. Query optimization and database-side pagination are planned improvements for larger datasets.

## Testing

Tests use Pytest and FastAPI's test client.

Run the complete suite:

```powershell
python -m pytest -v
```

Or use a compact summary:

```powershell
python -m pytest -q
```

The current development checkpoint has reported **67 passing tests**. Re-run the suite after changes; test counts may increase as new tests are added.

### Test database safety

Use a dedicated test database, such as `nearmates_test_db`. Never point destructive test fixtures at a development or production database. Keep test credentials and secrets out of source control.

## Roadmap

- [x] User registration and JWT authentication
- [x] PostgreSQL and SQLAlchemy integration
- [x] Alembic migrations
- [x] Language and interest catalogues
- [x] User preference endpoints
- [x] Initial discovery and compatibility scoring
- [x] Initial automated test suite
- [ ] Redis caching and cache invalidation
- [ ] Discovery query and pagination optimization
- [ ] Docker Compose setup
- [ ] Continuous integration with GitHub Actions
- [ ] Structured logging and observability
- [ ] Deployment and production configuration
- [ ] Connection requests and friend-management workflow

## Security Notes

- Never commit `.env`, passwords, JWT secrets, or production credentials.
- Use a strong, randomly generated secret for JWT signing.
- Keep password hashes out of API responses and logs.
- Require authentication for user-specific operations.
- Validate all client-supplied IDs and input values.
- Use a separate database for automated tests.
- Review migration scripts before applying them.
- Before production, add appropriate rate limiting, logging, monitoring, deployment secrets, and security review.

## Learning Goals

This project is intended to build practical experience with:

- REST API design and validation.
- Authentication and authorization.
- Relational database modeling and many-to-many relationships.
- SQLAlchemy ORM and SQL queries.
- Database migrations.
- Automated testing and regression prevention.
- Caching and cache invalidation.
- Performance analysis and deployment practices.

---

**NearMates is a work in progress.** Features described as planned should not be considered implemented until they are added, tested, and documented in the repository.
