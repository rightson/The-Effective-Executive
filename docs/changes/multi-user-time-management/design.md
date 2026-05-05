# Design: stack & multi-tenancy

## 1. Stack comparison

The user asked: should we move to **Next.js + Drizzle ORM + Postgres** or stay on **FastAPI + SQLAlchemy + (now) Postgres**?

| Concern | FastAPI + SQLAlchemy + Postgres (current+) | Next.js + Drizzle + Postgres |
|---|---|---|
| **Language continuity** | Python; same as today's `main.py`. Zero rewrite of domain logic. | Full TypeScript rewrite of every model, schema, endpoint. |
| **Lines of code to reach multi-user** | ~+300 (auth, user_id, Alembic). | ~+3,000 (re-implement five modules, dashboard, analysis). |
| **ORM ergonomics** | SQLAlchemy 2.x typed sessions; mature. | Drizzle is excellent — fully typed SQL, lighter than Prisma. |
| **Migrations** | Alembic — battle-tested, autogenerate works. | drizzle-kit — fast, simple, but newer. |
| **Auth** | Add `fastapi-users` or hand-rolled session cookie + argon2. | NextAuth / Auth.js — turnkey, but couples to Next routing. |
| **Frontend** | Today: vanilla JS in `static/`. Stays simple; no build step. | Next.js gives SSR, RSC, and a real component model — better long-term UX, much heavier toolchain. |
| **API shape** | Stays `GET /api/...`; OpenAPI free at `/docs`. | API routes via `app/api/.../route.ts`; OpenAPI not free. |
| **Deploy** | One Python process + Postgres. Fly/Render/own VM trivially. | Vercel-shaped; self-host needs Node + a process model. |
| **Background jobs** (future digests, reminders) | Celery/RQ/APScheduler in same Python ecosystem. | Needs a separate worker (Inngest, Trigger.dev, or a Node script). |
| **Type safety end-to-end** | Pydantic models + TS client (codegen from OpenAPI). Two languages. | Single TS codebase; tRPC or server actions give true E2E types. |
| **Risk of regression** | Low — incremental change to a working app. | High — re-implementing 500 lines of carefully-shaped domain logic. |
| **Time to ship multi-user MVP** | ~1–2 days. | ~1–2 weeks. |

### Verdict
**Keep FastAPI + SQLAlchemy. Switch SQLite → Postgres. Add Alembic. Layer auth.**

Reasons:
1. The methodology is the product. A rewrite spends weeks moving the working domain logic into a new language for no methodology gain.
2. Next.js's strongest cards (SSR, RSC, file-based routing, edge) don't help a structured-journal app whose UI is a handful of forms and tables.
3. If/when the SPA needs to become a real app (mobile-friendly, offline, richer charts), front it with **Next.js as a pure client** talking to the FastAPI backend. That keeps Drucker logic in one place and lets the UI evolve independently.
4. Drizzle is a great ORM but its main win — TS-end-to-end — only pays off in a TS backend. Adopting it forces the full rewrite.

### When to revisit
Switch to Next.js + Drizzle if **two** of the following become true:
- We need SSR'd, SEO-relevant pages (e.g. public profile pages).
- The team standardises on TypeScript and Python becomes the odd one out.
- We add real-time features that benefit from RSC + websockets (Liveblocks-style).

## 2. Multi-tenancy model

- **Tenant unit:** `user`. An `org` exists only to scope read-only manager views.
- **Isolation:** every domain row carries `user_id NOT NULL` with an index. All queries filter by `current_user.id`. No row-level security in v1; enforced in the application layer.
- **Manager view:** `org_memberships(user_id, org_id, role)` where role ∈ `{member, manager}`. A manager `GET /api/dashboard?user_id=<report>` succeeds iff the target shares an org and the manager has `role=manager`.
- **Auth:** session cookie (`HttpOnly`, `Secure`, `SameSite=Lax`), argon2 password hashes, CSRF via double-submit token on state-changing requests.
- **Sessions:** server-side session table (`id, user_id, created_at, expires_at, revoked_at`) — simpler than JWT for this surface area and trivially revocable.

## 3. Migration from SQLite

A one-shot script `scripts/import_sqlite.py` reads `effective_executive.db`, prompts for an account, and inserts every row under that `user_id`. Not part of the runtime path.

## 4. Open questions
- Do we want invite links for org joining, or admin-controlled add? (Default: invite links, expiring.)
- Is there ever a global "team time block" rollup, or strictly per-user with a manager peek? (Default: per-user only in v1.)
