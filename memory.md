# Memory

- Local Python environment: `.venv` at repo root; use `/Users/samirpatil/Desktop/Dev/os360-service/.venv/bin/python` for Django commands.
- Local boot path: create `.env` with `DB_ENGINE=sqlite3`, run `makemigrations users` if needed, then `migrate` and `runserver`.
- Health endpoint responds at `GET /health` once the dev server is running.
