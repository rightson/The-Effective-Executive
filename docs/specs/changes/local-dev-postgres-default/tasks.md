---
status: active
created: 2026-05-07
---

# Tasks

- [ ] Add `.env.example` with `DATABASE_URL`, `SESSION_TTL_DAYS`, `SECURE_COOKIES`, optional Google OAuth keys.
- [ ] Add `.env` to `.gitignore`.
- [ ] Add stdlib `.env` parser + loader in `manage.py` (no new dep — manage.py is stdlib-only by design).
- [ ] Add `db init` subcommand to `manage.py`: copy `.env.example` to `.env` if missing, load env, bootstrap Postgres role/db (interactive admin URL prompt), run `alembic upgrade head`.
- [ ] Make `manage.py run`, `dev`, and `db <alembic>` call the `.env` loader before spawning the venv python.
- [ ] Add a stdlib `.env` loader at the top of `main.py` so direct `uvicorn main:app` invocations also see the file.
- [ ] Flip default `DATABASE_URL` in `main.py` and `migrations/env.py` from `sqlite:///./effective_executive.db` to `postgresql://ee:ee@localhost:5432/effective_executive`.
- [ ] Update `manage.py` module docstring to reflect the new default and the `db init` command.
- [ ] Smoke test from clean state: `docker compose up -d` → `python3 manage.py db init` → `python3 manage.py run`.
- [ ] On accept: apply spec delta to `docs/specs/platform/spec.md` and mark this change `done`.
