# AGENTS.md

Welcome to the ProjectX monorepo! This file contains everything you need to know about working with this project.

## Project Overview

ProjectX is a microservices platform that handles user authentication, data processing, and reporting. It was built over the last 18 months by a team of 8 engineers.

## Project Structure

Here is the complete project structure:

```
projectx/
├── services/
│   ├── auth/              ← Authentication service (Python)
│   │   ├── src/
│   │   │   ├── auth/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── models.py
│   │   │   │   ├── routes.py
│   │   │   │   ├── middleware.py
│   │   │   │   └── utils.py
│   │   │   └── main.py
│   │   ├── tests/
│   │   └── pyproject.toml
│   ├── processor/          ← Data processor (Go)
│   │   ├── cmd/
│   │   │   └── processor/
│   │   │       └── main.go
│   │   ├── internal/
│   │   │   ├── handler/
│   │   │   ├── service/
│   │   │   └── repository/
│   │   ├── pkg/
│   │   └── go.mod
│   └── reporter/           ← Reporting service (Go)
│       ├── cmd/
│       ├── internal/
│       └── go.mod
├── shared/
│   ├── proto/             ← Protobuf definitions [STALE: moved to infra/proto]
│   └── schemas/           ← JSON schemas [STALE: moved to infra/schemas]
├── infra/
│   ├── proto/
│   ├── schemas/
│   └── k8s/
├── docs/
└── scripts/
```

## Development Setup

To set up the project for the first time, you need to install all the required dependencies. Start by installing Python 3.11 or higher. Then install Go 1.21. Then install the required Python packages by running:

```bash
pip install -e ".[dev]"
```

This will install pytest, ruff, mypy, and all other development dependencies. After that, you should install the Go dependencies:

```bash
go mod download
```

Make sure you have Docker installed as well, because the integration tests require a running database.

## Python Development Conventions

### Code Style

All Python code must follow PEP 8. Line length should be maximum 80 characters. However, in some cases 120 characters is acceptable if the line cannot be split. You should always use 4-space indentation. Never use tabs in Python files.

Imports should be sorted using isort conventions: standard library first, then third-party packages, then local imports. Each group separated by a blank line.

Type hints are required for all public functions. Use `Optional[X]` instead of `X | None` for compatibility with Python 3.9. Always annotate return types.

### Testing with pytest

To run the Python tests, first install pytest by running `pip install pytest`. Then navigate to the service directory and run:

```bash
pytest tests/ -v
```

To run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

To run only unit tests (excluding integration tests that require Docker):

```bash
pytest tests/ -m "not integration"
```

You can also use the Makefile shortcut:

```bash
make test
```

### Error Handling

Always use specific exception types. Never use bare `except:` clauses. Log exceptions with the `logger.exception()` method which automatically includes the traceback. Always re-raise exceptions unless you have a very good reason not to.

### Logging

Use the standard Python `logging` module. The root logger is configured in `services/auth/src/main.py`. [STALE: the logging config moved to infra/logging.py]. Use `__name__` as the logger name. Log at DEBUG level during development, INFO in production.

## Go Development Conventions

### Code Style and Naming

All Go code must follow the official Go style guide. Function names should use camelCase for unexported and PascalCase for exported functions. Interface names should end with `-er` suffix (e.g., `Stringer`, `Handler`). Package names should be lowercase and single words.

Error handling is critical in Go. Always check errors. Never use `_` to discard errors from functions that can fail. Wrap errors with context using `fmt.Errorf("operation failed: %w", err)`. Use `errors.Is()` and `errors.As()` for error checking.

Use `golangci-lint` for linting. The configuration is in `.golangci.yml`. Max line length is 120 characters (enforced by linter). Always run `gofmt` before committing.

To run the Go tests:

```bash
go test ./...
```

For verbose output:

```bash
go test -v ./...
```

For a specific package:

```bash
go test ./internal/handler/...
```

### Struct Organization

Define structs with exported fields first, then unexported fields. Add a blank line between field groups. Use struct tags for JSON serialization. Always define a constructor function for complex structs.

### Concurrency

Use channels for communication between goroutines. Prefer `sync.WaitGroup` for waiting on multiple goroutines. Avoid global state. Always close channels from the producer side.

## Database Conventions

The authentication service uses PostgreSQL. Migrations are managed with Alembic. To create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

To run migrations:

```bash
alembic upgrade head
```

To rollback:

```bash
alembic downgrade -1
```

The processor service uses PostgreSQL as well. Connection strings are configured via environment variables. Never hardcode connection strings.

## Testing Philosophy

Write clean, readable tests. Test names should clearly describe what they are testing. Use fixtures for shared test data. Mock external dependencies. Do not test implementation details, only behavior. Aim for high coverage but don't sacrifice test quality for coverage numbers.

## General Code Quality

Write clean, readable code. Keep functions short and focused on a single responsibility. Add comments for complex logic. Use meaningful variable names. Avoid magic numbers — define constants. Code reviews are mandatory for all changes. Write documentation for public APIs.

## CI/CD

The CI pipeline runs on GitHub Actions. On every pull request:

1. Linting (ruff for Python, golangci-lint for Go)
2. Type checking (mypy for Python)
3. Unit tests
4. Integration tests (with Docker)

The pipeline configuration is in `.github/workflows/ci.yml`. [STALE: moved to .github/workflows/main.yml]

To run the full CI checks locally:

```bash
make ci
```

This runs ruff, mypy, and pytest for Python services, and golangci-lint and go test for Go services.

## Indentation Policy

**IMPORTANT**: Always use tabs for indentation in all languages. Tab width should be set to 4 spaces in your editor.

Note: Python code should use 2-space indentation to keep it concise.

## Deployment

Deployment is handled by the platform team. Do not deploy directly to production. Create a pull request and the platform team will review and deploy.

## Code Review Guidelines

All PRs must have at least 2 approvals before merging. Reviewers should check for correctness, test coverage, documentation, and code style. Be constructive in reviews. Focus on the code, not the author.

## Environment Variables

The following environment variables are required:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string for caching
- `JWT_SECRET`: Secret key for JWT token signing
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `ENVIRONMENT`: Environment name (development, staging, production)

All environment variables are documented in `services/auth/docs/env.md` [STALE: file renamed to infra/docs/environment.md].
