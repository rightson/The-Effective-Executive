"""Import a legacy single-user effective_executive.db into a chosen account.

Usage:
    python scripts/import_sqlite.py path/to/effective_executive.db <email>

The target user must already exist (sign up via the SPA or API first).
All rows from the legacy DB are inserted under that user_id. Re-running
the script appends; it does not deduplicate.
"""
from __future__ import annotations

import sys
import sqlite3
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select  # noqa: E402

from main import (  # noqa: E402
    SessionLocal, UserDB,
    TimeEntryDB, ContributionDB, StrengthDB, PriorityDB, DecisionDB,
)


TABLES = {
    "time_entries": (TimeEntryDB, [
        "timestamp", "activity", "duration_minutes", "category",
        "worth_doing", "can_delegate", "wastes_others", "notes",
    ]),
    "contributions": (ContributionDB, [
        "created_at", "activity", "expected_outcome", "layer",
        "actual_outcome", "status",
    ]),
    "strengths": (StrengthDB, [
        "name", "description", "owner", "evidence", "created_at",
    ]),
    "priorities": (PriorityDB, [
        "title", "description", "future_oriented", "opportunity_not_problem",
        "own_direction", "high_meaning", "would_start_today", "status", "created_at",
    ]),
    "decisions": (DecisionDB, [
        "title", "problem_type", "boundary_conditions", "right_answer",
        "compromise", "assignee", "feedback_mechanism", "has_dissent",
        "status", "outcome", "created_at",
    ]),
}


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        return 2

    src_path, email = sys.argv[1], sys.argv[2]
    if not Path(src_path).exists():
        print(f"sqlite file not found: {src_path}", file=sys.stderr)
        return 1

    db = SessionLocal()
    try:
        user = db.scalar(select(UserDB).where(UserDB.email == email))
        if not user:
            print(f"no user with email {email!r} — sign up first", file=sys.stderr)
            return 1

        src = sqlite3.connect(src_path)
        src.row_factory = sqlite3.Row

        totals: dict[str, int] = {}
        for table, (model, cols) in TABLES.items():
            try:
                rows = src.execute(f"SELECT {', '.join(cols)} FROM {table}").fetchall()
            except sqlite3.OperationalError:
                rows = []
            for row in rows:
                kwargs = {c: row[c] for c in cols}
                kwargs["user_id"] = user.id
                db.add(model(**kwargs))
            totals[table] = len(rows)

        db.commit()
        for table, n in totals.items():
            print(f"  {table}: {n} rows imported")
        print(f"Imported into user_id={user.id} ({user.email})")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
