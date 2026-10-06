# Agentic Telegram Bot Builder

The repository is a Vercel-first monorepo.

- `frontend/` — Next.js web application
- `backend/` — FastAPI control-plane API
- Neon — PostgreSQL

## Development workflow

GitHub is the source of truth. Local execution is optional.

1. Push code to `main`.
2. Vercel creates a deployment.
3. Use the frontend deployment URL for browser testing.
4. Use the backend deployment URL + `/docs` for API testing.
5. Store production secrets only in Vercel Environment Variables.
6. Keep database migrations in `backend/alembic/versions`.

Phase 2 is implemented: authenticated users can create and manage persistent bot workspaces. Telegram, agent, and sandbox features remain deferred to their later phases.

## Vercel projects

Create two Vercel projects from this repository:

### Frontend
Root Directory: `frontend`
Framework: Next.js

Environment:
`NEXT_PUBLIC_API_URL=https://YOUR-BACKEND.vercel.app/api/v1`

### Backend
Root Directory: `backend`
Framework: FastAPI / Python
Entrypoint: `main.py`

Environment:
`DATABASE_URL`
`AUTH_SECRET`
`ENCRYPTION_KEY`
`ENVIRONMENT=production`
`SESSION_DAYS=7`
`SESSION_COOKIE_NAME=atbb_session`
`BACKEND_CORS_ORIGINS=https://YOUR-FRONTEND.vercel.app`

Apply the Alembic migration to the Neon database before testing registration.

## Phase 1 manual test

1. Open the frontend deployment.
2. Register a user.
3. Confirm redirect to `/dashboard`.
4. Refresh the page and confirm the session survives.
5. Sign out.
6. Sign in again.
7. Open the backend `/docs` endpoint and verify the health/auth endpoints.
