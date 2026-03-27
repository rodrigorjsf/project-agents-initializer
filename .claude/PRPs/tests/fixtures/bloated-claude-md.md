# CLAUDE.md

This file contains everything Claude needs to know when working on the ProjectX codebase.

## Project Overview

ProjectX is a microservices platform with authentication (Python/FastAPI), data processing (Go), and reporting (Go) services. The project uses a monorepo structure managed with Make.

## Architecture Summary

The system architecture follows a microservices pattern:

- `services/auth/` — FastAPI app handling JWT authentication, user management, OAuth2
- `services/processor/` — Go service consuming Kafka events and writing to PostgreSQL
- `services/reporter/` — Go service generating scheduled reports and sending emails
- `shared/schemas/` — Shared JSON schemas for inter-service communication [STALE: moved to infra/schemas/]
- `infra/` — Kubernetes manifests, Terraform configs, monitoring setup

Services communicate via gRPC (defined in `infra/proto/`) and async events via Kafka.

## Development Rules

When working on this project, always follow these rules:

1. Never modify database schema files directly — always use Alembic migrations
2. All API responses must use the standard response envelope: `{"data": ..., "meta": ...}`
3. Environment variables must be documented in `infra/docs/environment.md`
4. All new endpoints must have integration tests in addition to unit tests

### Formatting Rules

All Python files must have a maximum line length of 88 characters. Use double quotes for all Python strings. When formatting with Black, use the project's pyproject.toml settings.

For Go files, use `gofmt` formatting. Tab indentation only. Line length enforced by `golangci-lint` at 120 characters.

For TypeScript files (in the admin dashboard): use 2-space indentation, single quotes, semicolons required. Prettier config is in `apps/admin/.prettierrc`.

### Import Rules

Python imports must be sorted in this order:

1. Standard library imports
2. Third-party imports (with blank line separator)
3. Local imports (with blank line separator)

Use absolute imports only. Never use relative imports in this project.

Go imports must be grouped:

1. Standard library
2. External packages
3. Internal packages (github.com/projectx/...)

### Naming Conventions

Python:

- Classes: PascalCase
- Functions and variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Private attributes: _leading_underscore

Go:

- Exported: PascalCase
- Unexported: camelCase
- Constants: PascalCase (exported) or camelCase (unexported)
- Interfaces: end with -er suffix

### Comment Style

All functions and methods must have docstrings. Use Google-style docstrings for Python:

```python
def function(arg: str) -> bool:
    """Short description.

    Args:
        arg: Description of argument.

    Returns:
        Description of return value.
    """
```

For Go, use godoc-style comments:

```go
// FunctionName does X. It accepts Y and returns Z.
func FunctionName(y Type) ReturnType {
```

## Git Workflow Rules

These rules must be followed for all git operations:

1. Never commit directly to `main` or `develop` branches
2. Branch naming: `feature/TICKET-123-short-description`, `fix/TICKET-456-short-description`
3. Commit messages must follow Conventional Commits: `type(scope): description`
4. All commits must be signed with GPG keys
5. Squash commits before merging: maximum 3 commits per PR
6. PR descriptions must include: What changed, Why it changed, How to test

## Code Review Requirements

When reviewing or writing code for review:

- Always add inline comments explaining non-obvious logic
- Mark TODO comments with ticket numbers: `TODO(PROJ-123): Fix this`
- Never leave `console.log` or `fmt.Println` debug statements in code
- Performance-sensitive code must include benchmark comments

## Testing Requirements

Unit test coverage must be at least 80% for all services. Integration tests are required for all API endpoints. Test file names must end with `_test.py` (Python) or `_test.go` (Go). Test functions must start with `test_` (Python) or `Test` (Go).

Do not use `unittest.mock.patch` as a decorator — use it as a context manager only.

## Build and Run Commands

### Authentication Service (Python)

To run the auth service locally:

```bash
cd services/auth
uvicorn src.main:app --reload --port 8001
```

To run with Docker:

```bash
docker-compose up auth
```

Environment setup for first time:

```bash
cp .env.example .env
# Edit .env with your local values
uv sync
alembic upgrade head
```

### Processor Service (Go)

To run the processor service:

```bash
cd services/processor
go run cmd/processor/main.go
```

For development with hot reload:

```bash
air  # uses .air.toml config
```

### Running All Services

```bash
make dev  # starts all services with docker-compose
make dev-stop  # stops all services
```

## Environment Variables

Required variables (see `services/auth/docs/env.md` for details) [STALE: file moved to infra/docs/environment.md]:

| Variable | Service | Description |
| -------- | ------- | ----------- |
| `DATABASE_URL` | auth, processor | PostgreSQL connection string |
| `REDIS_URL` | auth | Redis for session storage |
| `KAFKA_BROKERS` | processor, reporter | Kafka broker addresses |
| `JWT_SECRET` | auth | JWT signing secret (min 32 chars) |
| `SMTP_HOST` | reporter | SMTP server for email sending |

## Dependency Management

Python dependencies are managed with `uv`. Never use `pip install` directly. Always add dependencies to `pyproject.toml`:

```bash
uv add package-name  # runtime dependency
uv add --dev package-name  # dev dependency
```

Go dependencies use Go modules. Never vendor dependencies (the `.gitignore` excludes vendor/):

```bash
go get github.com/package/name
go mod tidy  # clean up unused dependencies
```

## Security Rules

These security rules are inline here but should really be in `.claude/rules/security.md`:

1. Never log authentication tokens, passwords, or PII
2. Always validate and sanitize user input before processing
3. Use parameterized queries — never string interpolation in SQL
4. JWT tokens expire in 1 hour — do not extend this
5. Rate limiting is enforced at the nginx level — do not add application-level rate limiting
6. All secrets must be in environment variables — never in code or config files committed to git

## Monitoring and Observability

Metrics are exported via Prometheus. Dashboards are in Grafana. Traces use OpenTelemetry.

When adding new features, add appropriate metrics using the `metrics` package in `shared/metrics/` [STALE: package moved to infra/metrics/].

## Claude-Specific Instructions

When Claude makes changes to this codebase:

1. Read the AGENTS.md file first if it exists
2. Always run the full test suite before declaring work complete
3. If you cannot run tests, explain why and what manual verification is needed
4. When in doubt about architecture decisions, create a design doc in `docs/decisions/`
5. Use @nonexistent-module.md for additional context on the module system [STALE: file never existed]
6. Always check `infra/docs/conventions.md` before making infrastructure changes [STALE: file does not exist]

## Write Clean Code

Write clean, readable code. Keep functions small. Use meaningful names. Add comments when logic is complex. Follow the principle of least surprise. Code for the next developer, not just the current task. Review your own code before submitting for review. Test edge cases. Handle errors gracefully.
