# CLAUDE.md

NodeAPI is a TypeScript/Node.js REST API for user management and SaaS billing.

## Project Conventions

### TypeScript

Strict mode is enabled. No `any` types — use `unknown` for truly dynamic values. All async functions must handle errors (no floating promises). Use `zod` for runtime validation of external inputs (API requests, environment variables).

Prefer `type` over `interface` for object shapes unless you need declaration merging. Exports: named exports only, no default exports.

### Formatting Rules

Use 2-space indentation in all files. Single quotes for strings. Semicolons required. Prettier handles formatting — run `npm run format` before committing. Max line length is 100 characters.

### File Naming

- Route files: `kebab-case.routes.ts`
- Service files: `kebab-case.service.ts`
- Repository files: `kebab-case.repository.ts`
- Test files: `*.test.ts` co-located with source

## Development Workflow

### Running the API

```bash
npm run dev          # Development with hot reload (tsx watch)
npm run build        # Compile to dist/
npm start            # Run compiled output
```

### Testing

```bash
npm test             # Run all tests (Vitest)
npm run test:ui      # Open Vitest UI
npm run test:coverage  # With coverage report
```

Tests use an in-memory SQLite database (not PostgreSQL). When writing tests, import the test database client from `src/test/db.ts`, not the main `src/db.ts`.

### Database Workflow

```bash
npm run db:migrate        # Apply migrations
npm run db:migrate:create  # Create new migration
npm run db:seed           # Seed with test data
npm run db:reset          # Drop + recreate + seed
```

Prisma schema is in `prisma/schema.prisma`. Always run `npm run generate` after schema changes to update the TypeScript client.

## Common Patterns

### AppError Usage

Use `AppError` for all operational errors:

```typescript
throw new AppError(404, 'User not found', 'USER_NOT_FOUND');
```

Constructor: `AppError(statusCode, message, code)`.

### Logging

Use the logger from `src/lib/logger.ts` (wraps Winston). Log at appropriate levels:

- `logger.info()` — Successful operations, state changes
- `logger.warn()` — Recoverable issues, deprecations
- `logger.error()` — Errors that need attention

Never log passwords, tokens, or card numbers.

## Important Constraints

- Stripe webhooks must be verified with `stripe.webhooks.constructEvent()` — never trust webhook data without verification
- The soft-delete pattern is manual — always include `deletedAt: null` in queries for active records (see `src/config.js` for the Prisma middleware that logs missing filters) [note: file is actually `src/config.ts`]
- BullMQ job processors must be idempotent — jobs can be retried
- Database migrations are irreversible in production — always test rollback locally first
