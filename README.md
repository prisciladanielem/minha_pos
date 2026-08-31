# Minha Pós

An application for tracking practical training requirements in Nursing postgraduate programs, initially focused on Obstetric Nursing.

## About the Project

Minha Pós helps postgraduate students organize and track the practical requirements they need to complete during their training.

The application allows students to:

- See the requirements they need to complete
- Track their progress for each requirement
- Record activities they have completed
- Keep a history of their activities
- Optionally attach supporting evidence to an activity
- Track requirements based on different measurement types, such as hours, days, or quantities

The application is designed to support different postgraduate programs and institutions.

A postgraduate program at one institution may have completely different requirements from a program at another institution. Therefore, requirements are associated with a specific program rather than being hardcoded for a particular course.

### Example

A program may require:

- 4 hours in a rooming-in unit
- 20 assisted births
- 5 days in a specific activity

The student can record each completed activity and the application calculates the progress toward the corresponding requirement.

Supporting evidence is optional. When used, the most common type is expected to be an image/photo of a signed document.

## Core Domain

The initial domain model consists of the following entities.

### User

Represents an application user.

A user can have one or more enrollments.

### Institution

Represents an educational institution.

An institution can offer multiple postgraduate programs.

### Program

Represents a specific postgraduate program offered by an institution.

Requirements belong to a program.

### Enrollment

Represents a user's enrollment in a specific program.

This allows the application to support multiple enrollments for the same user and preserve enrollment history.

### ProgramRequirement

Represents a requirement that must be completed as part of a program.

A requirement has a target value and a measurement type.

Initial measurement types:

- `hours`
- `count`
- `days`

### Activity

Represents an activity performed by a student to fulfill a program requirement.

An activity belongs to a specific enrollment and a specific requirement.

### Evidence

Represents optional supporting evidence associated with an activity.

The initial use case is an image/photo of a signed document.

## Domain Relationships

    Institution 1 ──── N Program

    User 1 ──── N Enrollment N ──── 1 Program

    Program 1 ──── N ProgramRequirement

    Enrollment 1 ──── N Activity

    ProgramRequirement 1 ──── N Activity

    Activity 1 ──── 0..N Evidence

An important domain rule is that an `Activity` must belong to an `Enrollment`.

A `ProgramRequirement` describes what a program requires, while an `Activity` represents what a specific student has actually completed.

## Architecture

The backend follows **Onion Architecture with selective rigor**.

The main architectural principle is that the domain should remain independent from frameworks, databases, and infrastructure details.

    ┌──────────────────────────────────────────┐
    │                  API                     │
    │               FastAPI                    │
    │                                          │
    │   ┌──────────────────────────────────┐   │
    │   │          Application             │   │
    │   │                                  │   │
    │   │            Use Cases             │   │
    │   │              Ports               │   │
    │   │                                  │   │
    │   │   ┌──────────────────────────┐   │   │
    │   │   │          Domain          │   │   │
    │   │   │                          │   │   │
    │   │   │ Entities                 │   │   │
    │   │   │ Value Objects            │   │   │
    │   │   │ Domain Services          │   │   │
    │   │   └──────────────────────────┘   │   │
    │   └──────────────────────────────────┘   │
    │                                          │
    │              Infrastructure              │
    │                                          │
    │       PostgreSQL / Storage / ORM         │
    └──────────────────────────────────────────┘

The architecture intentionally does not apply the same level of abstraction to every part of the application.

Business-critical logic, especially:

    Activity
        ↓
    Progress
        ↓
    Requirement completion

will receive stronger domain boundaries and testing.

Simple CRUD operations will remain simpler when additional abstraction does not provide a meaningful benefit.

## Project Structure

    minha-pos/
    │
    ├── backend/
    │   ├── app/
    │   │   ├── domain/
    │   │   │   ├── entities/
    │   │   ├── value_objects/
    │   │   └── services/
    │   │
    │   ├── application/
    │   │   ├── ports/
    │   │   └── use_cases/
    │   │
    │   ├── infrastructure/
    │   │   ├── db/
    │   │   ├── repositories/
    │   │   └── storage/
    │   │
    │   └── api/
    │       ├── routes/
    │       ├── schemas/
    │       └── dependencies.py
    │
    ├── tests/
    │   ├── unit/
    │   │   ├── domain/
    │   │   └── application/
    │   ├── integration/
    │   │   └── infrastructure/
    │   └── e2e/
    │       └── api/
    │
    ├── alembic/
    ├── requirements.txt
    ├── Dockerfile
    └── .env.example

    ## Technology Stack

### Frontend

- Flutter
- Dart

### Backend

- Python
- FastAPI
- Pydantic

### Database

- PostgreSQL
- SQLAlchemy
- Alembic

### Infrastructure

- Docker
- Docker Compose

### Storage

Object storage will be used for supporting evidence files.

The database will store metadata and a storage reference rather than the binary file itself.

## Why PostgreSQL?

PostgreSQL was chosen over MongoDB because the domain has strong and well-defined relationships.

The main reasons are:

- Strong referential integrity
- Foreign keys between domain entities
- Transactional consistency
- Relational queries
- Aggregations for progress calculation
- A relatively stable schema

Progress is fundamentally a relational aggregation:

    Enrollment
        +
    ProgramRequirement
        +
    SUM(Activity.quantity)
        ↓
    Current Progress

This is a natural fit for PostgreSQL.

MongoDB could technically implement the same system, but its document-oriented model does not provide a meaningful advantage for this domain.

## Why FastAPI?

FastAPI was chosen because the backend is primarily an API consumed by the Flutter application.

It provides:

- Native Python type hints
- Request/response validation with Pydantic
- Automatic OpenAPI documentation
- Async support when needed
- Minimal framework constraints
- Flexibility to implement the desired architecture

Django is a valid alternative, especially when features such as Django Admin and a batteries-included ecosystem are priorities.

However, FastAPI fits better with the planned API-first architecture and keeps the framework separate from the domain.

## Database Design

The initial database will contain:

    users
    institutions
    programs
    enrollments
    program_requirements
    activities
    evidence

### Users

    users
    ├── id
    ├── name
    ├── email
    ├── password_hash
    ├── email_verified_at
    ├── created_at
    └── updated_at

Passwords are never stored in plain text.

### Institutions

    institutions
    ├── id
    ├── name
    ├── created_at
    └── updated_at

### Programs

    programs
    ├── id
    ├── institution_id
    ├── name
    ├── description
    ├── created_at
    └── updated_at

### Enrollments

    enrollments
    ├── id
    ├── user_id
    ├── program_id
    ├── status
    ├── start_date
    ├── end_date
    ├── created_at
    └── updated_at

### Program Requirements

    program_requirements
    ├── id
    ├── program_id
    ├── name
    ├── description
    ├── measurement_type
    ├── target_value
    ├── created_at
    └── updated_at

### Activities

    activities
    ├── id
    ├── enrollment_id
    ├── program_requirement_id
    ├── date
    ├── quantity
    ├── notes
    ├── created_at
    └── updated_at

### Evidence

    evidence
    ├── id
    ├── activity_id
    ├── storage_key
    ├── file_type
    ├── created_at
    └── updated_at

    ## Progress Calculation

Progress will initially be calculated from activities rather than persisted as independent state.

For example:

    Requirement:
    20 births

    Activities:
    5 births
    3 births
    4 births

    Current progress:
    12 / 20

    Remaining:
    8

The application can determine whether the requirement is complete:

    current >= target

The progress itself is derived data and should not be stored separately unless a future performance requirement justifies it.

## Application Layer

Application logic will be organized around use cases rather than generic services.

Examples:

    create_activity.py
    register_enrollment.py
    get_program_progress.py
    upload_evidence.py

A use case should:

- Receive its dependencies through ports
- Execute one application-level operation
- Work with domain entities
- Avoid direct dependencies on FastAPI
- Avoid direct dependencies on SQLAlchemy
- Avoid using Pydantic models as domain entities

## Ports and Repositories

Ports will be defined in the application layer.

Python `Protocol` will be preferred over abstract base classes where appropriate.

Example conceptual dependency:

    Application Use Case
            │
            ▼
          Port
            │
            ▼
    Infrastructure Adapter
            │
            ▼
       PostgreSQL

Repositories will be specific to the operations they need.

The project will avoid a generic repository such as `Repository<T>` when it would only reproduce functionality already provided by SQLAlchemy.

Instead, repositories should expose meaningful operations such as:

    get_activities_for_requirement()

rather than generic abstractions such as:

    find_by()

## SQLAlchemy

SQLAlchemy ORM models will be kept separate from domain entities.

    Domain Entity
         ↕
    Repository Mapping
         ↕
    SQLAlchemy Model
         ↕
    PostgreSQL

This keeps the domain independent from the persistence framework.

## Authentication

The application will support:

- User registration
- Email and password login
- Password hashing
- Authentication of protected routes
- Email verification
- Password recovery

The initial authentication strategy will use a short-lived access token.

Refresh-token behavior may be introduced later if needed.

## Evidence and File Storage

Evidence is optional.

The expected primary use case is:

    Register Activity
           ↓
    Optional Evidence
           ↓
    Take photo / select image
           ↓
    Upload
           ↓
    Store file
           ↓
    Save storage reference

The domain should not know whether the file is stored in:

- Local storage
- Amazon S3
- Google Cloud Storage
- Another object-storage provider

The application will depend on a storage port.

Concrete implementations will live in:

    infrastructure/storage/

## API

The backend will expose a REST API consumed by the Flutter application.

Initial API areas include:

    /auth
    /enrollments
    /programs
    /requirements
    /activities
    /evidence
    /users

API schemas will be defined separately from domain entities.

FastAPI will be responsible for:

- HTTP routing
- Request validation
- Authentication dependencies
- Serialization
- HTTP error handling
- OpenAPI documentation

## Frontend

The frontend will be implemented using Flutter.

The application will follow the visual design defined in the product prototypes.

Initial screens and flows include:

- Welcome
- Login
- Home / Progress
- Requirement details
- Register activity
- Activity registered
- Activity history
- Activity details
- Requirement nearly completed
- Requirement completed
- Training completed

Frontend implementation will consume the real backend API rather than relying on permanent mock data.

## Testing Strategy

The project will use multiple testing levels.

### Unit Tests

Focus on domain rules and application use cases.

    tests/unit/
    ├── domain/
    └── application/

Examples:

- Progress calculation
- Requirement completion
- Measurement types
- Activity validation
- Use case behavior

### Integration Tests

Test infrastructure components against PostgreSQL.

    tests/integration/
    └── infrastructure/

Examples:

- SQLAlchemy mappings
- Repository behavior
- Database constraints
- Alembic migrations

### End-to-End API Tests

Test the API through FastAPI.

    tests/e2e/
    └── api/

Examples:

- User registration
- Authentication
- Creating an enrollment
- Registering an activity
- Retrieving progress
- User data isolation

## Development Principles

### Keep the domain independent

The domain should not depend on:

- FastAPI
- SQLAlchemy
- PostgreSQL
- Flutter
- Cloud storage providers

### Prefer simple abstractions

Abstractions should exist because they provide a real benefit, not simply because the architecture diagram contains a layer.

### Test business rules

The most important business logic should be testable without requiring a database or HTTP server.

### Avoid premature optimization

Progress will initially be calculated from persisted activities.

Caching, materialized views, event-driven processing, and other optimizations should only be introduced when justified by actual requirements.

### Build incrementally

The project will be developed in small, testable milestones.

## Milestones

### M1 — Project Foundation

- Project structure
- Python environment
- FastAPI
- PostgreSQL
- Docker Compose
- SQLAlchemy
- Alembic
- Health check
- Initial visual assets

### M2 — Database and Domain

- Domain entities
- Database models
- Relationships
- Migrations
- Seed data
- Persistence tests

### M3 — Authentication

- Registration
- Login
- Password hashing
- Authentication
- User identity
- Email verification
- Password recovery

### M4 — Requirements and Progress

- Requirement retrieval
- Activity registration
- `count` requirements
- `hours` requirements
- `days` requirements
- Progress calculation
- Requirement completion
- Activity history

### M5 — Evidence

- Image upload
- Evidence association
- Evidence retrieval
- Object storage
- File validation

### M6 — Flutter

- Welcome
- Login
- Home / Progress
- Requirement details
- Activity registration
- Activity success
- History
- Activity details
- Requirement completion states
- Training completion
- API integration

### M7 — Quality and Deployment

- Unit tests
- Integration tests
- End-to-end tests
- Security review
- Logging
- Error handling
- CI/CD
- Staging environment
- Initial deployment

## Project Status

🚧 **In development**

The project is currently in the initial foundation phase.

## Documentation

The detailed product and architecture specification is maintained separately from this README.

The README is intended to provide a high-level overview of:

- What the project does
- How it is structured
- Which technologies are used
- How the application is expected to evolve

## Running tests

Before running the test suite, make sure the database schema is up to date:

```bash
alembic upgrade head
```

Then run the tests:

```bash
pytest
```