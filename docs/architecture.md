# Architecture

Next.js is the UI/control client. FastAPI is the control-plane API. PostgreSQL/Neon stores application state. Generated bot code will never execute inside FastAPI; later phases will execute it only inside Vercel Sandbox.

Current lifecycle:
Authentication -> Bot Workspace -> Telegram credentials -> Agent chat -> LangGraph -> code generation -> Sandbox -> tests -> Telegram testing -> versioning.
