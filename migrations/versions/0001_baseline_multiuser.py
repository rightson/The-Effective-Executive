"""baseline multi-user schema

Creates accounts (users, sessions, orgs, org_memberships) and the five
domain tables with user_id scoping. Equivalent to Base.metadata.create_all
on an empty database.

Revision ID: 0001_baseline
Revises:
Create Date: 2026-05-05
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


revision = "0001_baseline"
down_revision = None
branch_labels = None
depends_on = None


def _user_fk():
    return sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE")


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(200), server_default=""),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "sessions",
        sa.Column("token", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("csrf_token", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        _user_fk(),
    )
    op.create_index("ix_sessions_user_id", "sessions", ["user_id"])

    op.create_table(
        "orgs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )

    op.create_table(
        "org_memberships",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("org_id", sa.Integer, nullable=False),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("role", sa.String(50), nullable=False, server_default="member"),
        sa.ForeignKeyConstraint(["org_id"], ["orgs.id"], ondelete="CASCADE"),
        _user_fk(),
        sa.UniqueConstraint("org_id", "user_id", name="uq_org_user"),
    )
    op.create_index("ix_org_memberships_org_id", "org_memberships", ["org_id"])
    op.create_index("ix_org_memberships_user_id", "org_memberships", ["user_id"])

    op.create_table(
        "time_entries",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("timestamp", sa.DateTime, server_default=sa.func.now()),
        sa.Column("activity", sa.String(500), nullable=False),
        sa.Column("duration_minutes", sa.Integer, nullable=False),
        sa.Column("category", sa.String(50), server_default="uncategorized"),
        sa.Column("worth_doing", sa.Boolean, nullable=True),
        sa.Column("can_delegate", sa.Boolean, nullable=True),
        sa.Column("wastes_others", sa.Boolean, nullable=True),
        sa.Column("notes", sa.Text, server_default=""),
        _user_fk(),
    )
    op.create_index("ix_time_entries_user_id", "time_entries", ["user_id"])

    op.create_table(
        "contributions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("activity", sa.String(500), nullable=False),
        sa.Column("expected_outcome", sa.Text, server_default=""),
        sa.Column("layer", sa.String(50), server_default="direct_results"),
        sa.Column("actual_outcome", sa.Text, server_default=""),
        sa.Column("status", sa.String(50), server_default="planned"),
        _user_fk(),
    )
    op.create_index("ix_contributions_user_id", "contributions", ["user_id"])

    op.create_table(
        "strengths",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text, server_default=""),
        sa.Column("owner", sa.String(200), server_default="self"),
        sa.Column("evidence", sa.Text, server_default=""),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        _user_fk(),
    )
    op.create_index("ix_strengths_user_id", "strengths", ["user_id"])

    op.create_table(
        "priorities",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("description", sa.Text, server_default=""),
        sa.Column("future_oriented", sa.Boolean, server_default=sa.false()),
        sa.Column("opportunity_not_problem", sa.Boolean, server_default=sa.false()),
        sa.Column("own_direction", sa.Boolean, server_default=sa.false()),
        sa.Column("high_meaning", sa.Boolean, server_default=sa.false()),
        sa.Column("would_start_today", sa.Boolean, nullable=True),
        sa.Column("status", sa.String(50), server_default="active"),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        _user_fk(),
    )
    op.create_index("ix_priorities_user_id", "priorities", ["user_id"])

    op.create_table(
        "decisions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("problem_type", sa.String(50), server_default="generic"),
        sa.Column("boundary_conditions", sa.Text, server_default=""),
        sa.Column("right_answer", sa.Text, server_default=""),
        sa.Column("compromise", sa.Text, server_default=""),
        sa.Column("assignee", sa.String(200), server_default=""),
        sa.Column("feedback_mechanism", sa.Text, server_default=""),
        sa.Column("has_dissent", sa.Boolean, server_default=sa.false()),
        sa.Column("status", sa.String(50), server_default="open"),
        sa.Column("outcome", sa.Text, server_default=""),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        _user_fk(),
    )
    op.create_index("ix_decisions_user_id", "decisions", ["user_id"])


def downgrade() -> None:
    for t in (
        "decisions", "priorities", "strengths", "contributions", "time_entries",
        "org_memberships", "orgs", "sessions", "users",
    ):
        op.drop_table(t)
