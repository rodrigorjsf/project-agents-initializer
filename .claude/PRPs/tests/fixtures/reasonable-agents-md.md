# AGENTS.md

NodeAPI is a REST API service built with Node.js, Express, and TypeScript. It handles user management and subscription billing for a SaaS product.

## Tech Stack

- **Runtime**: Node.js 20 LTS
- **Framework**: Express 4 + TypeScript
- **Database**: PostgreSQL via Prisma ORM
- **Queue**: BullMQ (Redis-backed job queues)
- **Auth**: JWT (access tokens 15min, refresh tokens 30 days)
- **Testing**: Vitest + supertest

## Development Commands

- `npm test` — Run all tests
- `npm run test:watch` — Watch mode
- `npm run db:migrate` — Apply pending migrations
- `npm run db:seed` — Seed development database
- `npm run generate` — Regenerate Prisma client after schema changes

## Architecture

The API follows a layered architecture:

- `src/routes/` — Express route handlers, input validation
- `src/services/` — Business logic, no direct database access
- `src/repositories/` — All database queries via Prisma
- `src/jobs/` — BullMQ job processors
- `src/middleware/` — Auth, error handling, logging

Keep this separation strict. Services must not import from routes; repositories must not import from services.

## Database Conventions

All database changes must go through Prisma migrations. Never modify the database directly.

Migration naming: `YYYYMMDD_short_description` (e.g., `20240115_add_subscription_status`).

When writing Prisma queries, use transactions for multi-table operations. The Prisma client is a singleton — import from `src/db.ts`.

Soft deletes are used for users and subscriptions. Always filter with `where: { deletedAt: null }` unless explicitly querying deleted records. Forgetting this filter is a common bug — the soft-delete pattern is not enforced by Prisma automatically.

## Error Handling

Handle errors appropriately throughout the codebase.

All unhandled promise rejections are caught by the global error handler in `src/middleware/errorHandler.ts`. Operational errors (user-facing) should use `AppError` with an HTTP status code. Programming errors (bugs) should be thrown as plain `Error` and will return 500.

## Authentication

JWT tokens use RS256 algorithm. Public/private keys are in `config/keys/`. The access token contains `userId`, `role`, and `sessionId`. The refresh token only contains `sessionId`.

Never include sensitive data in tokens — the token is not encrypted, only signed.

## Background Jobs

BullMQ queues are defined in `src/jobs/queues.ts`. Each job type has its own processor file in `src/jobs/processors/`. Jobs are retried 3 times with exponential backoff. Failed jobs after max retries go to the dead letter queue — monitor this in production.

## Environment Setup

Copy `.env.example` to `.env.local` and fill in values. Required:

- `DATABASE_URL` — Prisma connection string (includes pool config)
- `REDIS_URL` — BullMQ connection
- `JWT_PRIVATE_KEY_PATH` / `JWT_PUBLIC_KEY_PATH` — RSA key paths
- `STRIPE_SECRET_KEY` — Payment processing
