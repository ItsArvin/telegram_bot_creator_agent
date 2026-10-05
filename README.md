# Agentic Telegram Bot Builder

Phase 1 implements authentication on top of the Phase 0 monorepo.

## Phase 1

- PostgreSQL + SQLAlchemy async
- Alembic migration
- Argon2 password hashing via pwdlib
- Opaque, hashed, expiring sessions
- HttpOnly session cookie
- Register / Login / Logout / Me APIs
- Protected Next.js dashboard
- Monochrome UI

## Vercel development

The project is designed as a monorepo:
- `frontend/` -> Next.js deployment
- `backend/` -> FastAPI deployment
- Neon -> PostgreSQL

Local development is optional. The primary development workflow is GitHub -> Vercel preview deployments.

See `docs/development.md` for the phase plan.
