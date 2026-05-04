# The Effective Executive

A local, single-user web service that turns Peter Drucker's five executive habits into structured records you can review.

The service is opinionated: each module enforces the diagnostic Drucker prescribes for that habit, rather than giving you a free-form notes app. If a field exists, the book says you should be filling it in.

## The five modules

Each maps to one of the habits in *The Effective Executive* (1967).

**Time** — log activities with duration. For every entry, answer the three diagnostic questions: is it worth doing at all, could someone else do it as well, does it waste other people's time. Analysis surfaces total minutes, breakdown by category, and how many minutes sit in **consolidated blocks** of 90+ minutes (Drucker's threshold for usable knowledge work).

**Contributions** — every planned activity records the **expected outward outcome** before it starts, classified into one of the three layers: direct results, values, or talent development. An activity without a writeable expected outcome should not be done.

**Strengths** — register strengths (your own and others') with evidence. Used to assign work to the shape of the person, not patch their weaknesses.

**Priorities** — each priority is scored on Drucker's four criteria: future-oriented, opportunity over problem, own direction, high meaning. The **would_start_today** field is the systematic-abandonment prompt: if the answer is no, mark it for abandonment.

**Decisions** — five-step decision record: problem type (generic vs. unique), boundary conditions, the right answer, the compromise, the assignee, the feedback mechanism, and a `has_dissent` flag (Drucker: a decision with no dissent is probably wrong).

A `/api/dashboard` endpoint rolls these into one view, including how many priorities are flagged for abandonment and how many decisions still have no implementer.

## Run

```
python3 -m pip install -r requirements.txt
python3 main.py
```

Open http://localhost:8000 for the SPA, or http://localhost:8000/docs for the OpenAPI explorer.

Data lives in `effective_executive.db` (SQLite) in the working directory.

## API surface

| Resource | Endpoints |
|---|---|
| Time entries | `GET/POST/PUT/DELETE /api/time-entries`, `GET /api/time-entries/analysis` |
| Contributions | `GET/POST/PUT/DELETE /api/contributions` |
| Strengths | `GET/POST/PUT/DELETE /api/strengths` |
| Priorities | `GET/POST/PUT/DELETE /api/priorities` |
| Decisions | `GET/POST/PUT/DELETE /api/decisions` |
| Dashboard | `GET /api/dashboard` |

## Stack

FastAPI · SQLAlchemy 2.x · SQLite · vanilla JS SPA in [static/](static/).

No auth, no multi-user, no migrations. Schema changes require deleting the database file.

## Scope

Single-user, local-first. Designed to be the structured journal Drucker describes — not a team productivity platform. The methodology assumes the work itself has potential value; the service helps you execute, not decide whether to.
