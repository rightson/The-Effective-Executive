from fastapi import FastAPI, HTTPException, Depends, Request, Response, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, Text,
    ForeignKey, Index, UniqueConstraint, select,
)
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker, relationship
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
import secrets

# ─── Configuration ────────────────────────────────────────────────────────────

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./effective_executive.db")
SESSION_TTL_DAYS = int(os.environ.get("SESSION_TTL_DAYS", "30"))
SECURE_COOKIES = os.environ.get("SECURE_COOKIES", "false").lower() == "true"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ph = PasswordHasher()


class Base(DeclarativeBase):
    pass


# ─── Accounts ────────────────────────────────────────────────────────────────

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class SessionDB(Base):
    __tablename__ = "sessions"
    token = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    csrf_token = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)


class OrgDB(Base):
    __tablename__ = "orgs"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class OrgMembershipDB(Base):
    __tablename__ = "org_memberships"
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("orgs.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False, default="member")  # member | manager
    __table_args__ = (UniqueConstraint("org_id", "user_id", name="uq_org_user"),)


# ─── Domain models (now scoped to user_id) ───────────────────────────────────

class TimeEntryDB(Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    activity = Column(String(500), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    category = Column(String(50), default="uncategorized")
    worth_doing = Column(Boolean, nullable=True)
    can_delegate = Column(Boolean, nullable=True)
    wastes_others = Column(Boolean, nullable=True)
    notes = Column(Text, default="")


class ContributionDB(Base):
    __tablename__ = "contributions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    activity = Column(String(500), nullable=False)
    expected_outcome = Column(Text, default="")
    layer = Column(String(50), default="direct_results")
    actual_outcome = Column(Text, default="")
    status = Column(String(50), default="planned")


class StrengthDB(Base):
    __tablename__ = "strengths"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    owner = Column(String(200), default="self")
    evidence = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class PriorityDB(Base):
    __tablename__ = "priorities"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    future_oriented = Column(Boolean, default=False)
    opportunity_not_problem = Column(Boolean, default=False)
    own_direction = Column(Boolean, default=False)
    high_meaning = Column(Boolean, default=False)
    would_start_today = Column(Boolean, nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class DecisionDB(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    problem_type = Column(String(50), default="generic")
    boundary_conditions = Column(Text, default="")
    right_answer = Column(Text, default="")
    compromise = Column(Text, default="")
    assignee = Column(String(200), default="")
    feedback_mechanism = Column(Text, default="")
    has_dissent = Column(Boolean, default=False)
    status = Column(String(50), default="open")
    outcome = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


if os.environ.get("EE_SKIP_CREATE_ALL", "").lower() not in ("1", "true", "yes"):
    Base.metadata.create_all(bind=engine)


# ─── Pydantic schemas ────────────────────────────────────────────────────────

class SignupIn(BaseModel):
    email: EmailStr
    password: str
    display_name: str = ""

    @field_validator("password")
    @classmethod
    def _pw_len(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: str
    display_name: str
    model_config = {"from_attributes": True}


class TimeEntryCreate(BaseModel):
    activity: str
    duration_minutes: int
    category: str = "uncategorized"
    notes: str = ""


class TimeEntryUpdate(BaseModel):
    activity: Optional[str] = None
    duration_minutes: Optional[int] = None
    category: Optional[str] = None
    worth_doing: Optional[bool] = None
    can_delegate: Optional[bool] = None
    wastes_others: Optional[bool] = None
    notes: Optional[str] = None


class TimeEntryOut(BaseModel):
    id: int
    timestamp: datetime
    activity: str
    duration_minutes: int
    category: str
    worth_doing: Optional[bool]
    can_delegate: Optional[bool]
    wastes_others: Optional[bool]
    notes: str
    model_config = {"from_attributes": True}


class ContributionCreate(BaseModel):
    activity: str
    expected_outcome: str = ""
    layer: str = "direct_results"
    status: str = "planned"


class ContributionUpdate(BaseModel):
    activity: Optional[str] = None
    expected_outcome: Optional[str] = None
    layer: Optional[str] = None
    actual_outcome: Optional[str] = None
    status: Optional[str] = None


class ContributionOut(BaseModel):
    id: int
    created_at: datetime
    activity: str
    expected_outcome: str
    layer: str
    actual_outcome: str
    status: str
    model_config = {"from_attributes": True}


class StrengthCreate(BaseModel):
    name: str
    description: str = ""
    owner: str = "self"
    evidence: str = ""


class StrengthOut(BaseModel):
    id: int
    name: str
    description: str
    owner: str
    evidence: str
    created_at: datetime
    model_config = {"from_attributes": True}


class PriorityCreate(BaseModel):
    title: str
    description: str = ""
    future_oriented: bool = False
    opportunity_not_problem: bool = False
    own_direction: bool = False
    high_meaning: bool = False


class PriorityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    future_oriented: Optional[bool] = None
    opportunity_not_problem: Optional[bool] = None
    own_direction: Optional[bool] = None
    high_meaning: Optional[bool] = None
    would_start_today: Optional[bool] = None
    status: Optional[str] = None


class PriorityOut(BaseModel):
    id: int
    title: str
    description: str
    future_oriented: bool
    opportunity_not_problem: bool
    own_direction: bool
    high_meaning: bool
    would_start_today: Optional[bool]
    status: str
    created_at: datetime
    model_config = {"from_attributes": True}


class DecisionCreate(BaseModel):
    title: str
    problem_type: str = "generic"
    boundary_conditions: str = ""
    right_answer: str = ""
    compromise: str = ""
    assignee: str = ""
    feedback_mechanism: str = ""
    has_dissent: bool = False


class DecisionUpdate(BaseModel):
    title: Optional[str] = None
    problem_type: Optional[str] = None
    boundary_conditions: Optional[str] = None
    right_answer: Optional[str] = None
    compromise: Optional[str] = None
    assignee: Optional[str] = None
    feedback_mechanism: Optional[str] = None
    has_dissent: Optional[bool] = None
    status: Optional[str] = None
    outcome: Optional[str] = None


class DecisionOut(BaseModel):
    id: int
    title: str
    problem_type: str
    boundary_conditions: str
    right_answer: str
    compromise: str
    assignee: str
    feedback_mechanism: str
    has_dissent: bool
    status: str
    outcome: str
    created_at: datetime
    model_config = {"from_attributes": True}


# ─── App ─────────────────────────────────────────────────────────────────────

app = FastAPI(title="The Effective Executive")

SESSION_COOKIE = "ee_session"
CSRF_COOKIE = "ee_csrf"
CSRF_HEADER = "X-CSRF-Token"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _set_session_cookies(resp: Response, token: str, csrf: str) -> None:
    common = dict(httponly=True, samesite="lax", secure=SECURE_COOKIES,
                  max_age=SESSION_TTL_DAYS * 86400, path="/")
    resp.set_cookie(SESSION_COOKIE, token, **common)
    # CSRF cookie is readable by JS (not httponly) so SPA can echo it back.
    resp.set_cookie(CSRF_COOKIE, csrf, httponly=False, samesite="lax",
                    secure=SECURE_COOKIES, max_age=SESSION_TTL_DAYS * 86400, path="/")


def _clear_session_cookies(resp: Response) -> None:
    resp.delete_cookie(SESSION_COOKIE, path="/")
    resp.delete_cookie(CSRF_COOKIE, path="/")


def current_user(
    request: Request,
    db: Session = Depends(get_db),
    ee_session: Optional[str] = Cookie(default=None),
) -> UserDB:
    if not ee_session:
        raise HTTPException(401, "Not authenticated")
    sess = db.get(SessionDB, ee_session)
    if not sess or sess.expires_at < datetime.utcnow():
        raise HTTPException(401, "Session expired")

    # CSRF: required on state-changing methods.
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        # Allow auth/logout without CSRF only for the very first login flow.
        sent = request.headers.get(CSRF_HEADER)
        if not sent or not secrets.compare_digest(sent, sess.csrf_token):
            raise HTTPException(403, "Invalid CSRF token")

    user = db.get(UserDB, sess.user_id)
    if not user:
        raise HTTPException(401, "User not found")
    return user


# ─── Auth endpoints ──────────────────────────────────────────────────────────

@app.post("/api/auth/signup", response_model=UserOut, status_code=201)
def signup(payload: SignupIn, response: Response, db: Session = Depends(get_db)):
    existing = db.scalar(select(UserDB).where(UserDB.email == payload.email))
    if existing:
        raise HTTPException(409, "Email already registered")
    user = UserDB(
        email=payload.email,
        password_hash=ph.hash(payload.password),
        display_name=payload.display_name or payload.email.split("@")[0],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    _start_session(db, user, response)
    return user


@app.post("/api/auth/login", response_model=UserOut)
def login(payload: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(UserDB).where(UserDB.email == payload.email))
    if not user:
        raise HTTPException(401, "Invalid credentials")
    try:
        ph.verify(user.password_hash, payload.password)
    except VerifyMismatchError:
        raise HTTPException(401, "Invalid credentials")
    if ph.check_needs_rehash(user.password_hash):
        user.password_hash = ph.hash(payload.password)
        db.commit()
    _start_session(db, user, response)
    return user


@app.post("/api/auth/logout")
def logout(response: Response, db: Session = Depends(get_db),
           ee_session: Optional[str] = Cookie(default=None)):
    if ee_session:
        sess = db.get(SessionDB, ee_session)
        if sess:
            db.delete(sess)
            db.commit()
    _clear_session_cookies(response)
    return {"ok": True}


@app.get("/api/auth/me", response_model=UserOut)
def me(user: UserDB = Depends(current_user)):
    return user


def _start_session(db: Session, user: UserDB, response: Response) -> None:
    token = secrets.token_urlsafe(32)
    csrf = secrets.token_urlsafe(32)
    sess = SessionDB(
        token=token,
        user_id=user.id,
        csrf_token=csrf,
        expires_at=datetime.utcnow() + timedelta(days=SESSION_TTL_DAYS),
    )
    db.add(sess)
    db.commit()
    _set_session_cookies(response, token, csrf)


# ─── Org / manager view ──────────────────────────────────────────────────────

class OrgMemberOut(BaseModel):
    user_id: int
    email: str
    display_name: str
    org_id: int
    org_name: str
    role: str


@app.get("/api/org/members", response_model=List[OrgMemberOut])
def list_org_members(user: UserDB = Depends(current_user), db: Session = Depends(get_db)):
    """List members of orgs where the current user is a manager."""
    managed_orgs = db.scalars(
        select(OrgMembershipDB.org_id).where(
            OrgMembershipDB.user_id == user.id,
            OrgMembershipDB.role == "manager",
        )
    ).all()
    if not managed_orgs:
        return []
    rows = db.execute(
        select(OrgMembershipDB, UserDB, OrgDB)
        .join(UserDB, UserDB.id == OrgMembershipDB.user_id)
        .join(OrgDB, OrgDB.id == OrgMembershipDB.org_id)
        .where(OrgMembershipDB.org_id.in_(managed_orgs))
    ).all()
    out = []
    for membership, member, org in rows:
        if member.id == user.id:
            continue
        out.append(OrgMemberOut(
            user_id=member.id, email=member.email, display_name=member.display_name,
            org_id=org.id, org_name=org.name, role=membership.role,
        ))
    return out


def _assert_manager_can_view(db: Session, manager: UserDB, target_user_id: int) -> None:
    if target_user_id == manager.id:
        return
    shared = db.scalar(
        select(OrgMembershipDB.id)
        .where(
            OrgMembershipDB.user_id == manager.id,
            OrgMembershipDB.role == "manager",
            OrgMembershipDB.org_id.in_(
                select(OrgMembershipDB.org_id).where(OrgMembershipDB.user_id == target_user_id)
            ),
        )
        .limit(1)
    )
    if not shared:
        raise HTTPException(403, "Not authorised to view this user")


# ─── Time entries ────────────────────────────────────────────────────────────

@app.get("/api/time-entries/analysis")
def analyze_time(db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    entries = db.scalars(select(TimeEntryDB).where(TimeEntryDB.user_id == user.id)).all()
    if not entries:
        return {"total_minutes": 0, "by_category": {}, "diagnosis": {}, "consolidated_minutes": 0}

    total = sum(e.duration_minutes for e in entries)
    by_cat: dict = {}
    for e in entries:
        by_cat[e.category] = by_cat.get(e.category, 0) + e.duration_minutes

    diagnosed = [e for e in entries if e.worth_doing is not None]
    return {
        "total_minutes": total,
        "by_category": by_cat,
        "diagnosis": {
            "total_diagnosed": len(diagnosed),
            "worth_doing": sum(1 for e in diagnosed if e.worth_doing),
            "can_delegate": sum(1 for e in diagnosed if e.can_delegate),
            "wastes_others": sum(1 for e in diagnosed if e.wastes_others),
        },
        "consolidated_minutes": sum(e.duration_minutes for e in entries if e.duration_minutes >= 90),
    }


@app.get("/api/time-entries", response_model=List[TimeEntryOut])
def list_time_entries(db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    return db.scalars(
        select(TimeEntryDB).where(TimeEntryDB.user_id == user.id).order_by(TimeEntryDB.timestamp.desc())
    ).all()


@app.post("/api/time-entries", response_model=TimeEntryOut, status_code=201)
def create_time_entry(entry: TimeEntryCreate, db: Session = Depends(get_db),
                      user: UserDB = Depends(current_user)):
    db_e = TimeEntryDB(user_id=user.id, **entry.model_dump())
    db.add(db_e); db.commit(); db.refresh(db_e)
    return db_e


def _own_or_404(db: Session, model, ident: int, user_id: int):
    obj = db.scalar(select(model).where(model.id == ident, model.user_id == user_id))
    if not obj:
        raise HTTPException(404, "Not found")
    return obj


@app.put("/api/time-entries/{entry_id}", response_model=TimeEntryOut)
def update_time_entry(entry_id: int, entry: TimeEntryUpdate,
                      db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    db_e = _own_or_404(db, TimeEntryDB, entry_id, user.id)
    for k, v in entry.model_dump(exclude_none=True).items():
        setattr(db_e, k, v)
    db.commit(); db.refresh(db_e)
    return db_e


@app.delete("/api/time-entries/{entry_id}")
def delete_time_entry(entry_id: int, db: Session = Depends(get_db),
                      user: UserDB = Depends(current_user)):
    db_e = _own_or_404(db, TimeEntryDB, entry_id, user.id)
    db.delete(db_e); db.commit()
    return {"ok": True}


# ─── Contributions ───────────────────────────────────────────────────────────

@app.get("/api/contributions", response_model=List[ContributionOut])
def list_contributions(db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    return db.scalars(
        select(ContributionDB).where(ContributionDB.user_id == user.id)
        .order_by(ContributionDB.created_at.desc())
    ).all()


@app.post("/api/contributions", response_model=ContributionOut, status_code=201)
def create_contribution(c: ContributionCreate, db: Session = Depends(get_db),
                        user: UserDB = Depends(current_user)):
    db_c = ContributionDB(user_id=user.id, **c.model_dump())
    db.add(db_c); db.commit(); db.refresh(db_c)
    return db_c


@app.put("/api/contributions/{cid}", response_model=ContributionOut)
def update_contribution(cid: int, c: ContributionUpdate, db: Session = Depends(get_db),
                        user: UserDB = Depends(current_user)):
    db_c = _own_or_404(db, ContributionDB, cid, user.id)
    for k, v in c.model_dump(exclude_none=True).items():
        setattr(db_c, k, v)
    db.commit(); db.refresh(db_c)
    return db_c


@app.delete("/api/contributions/{cid}")
def delete_contribution(cid: int, db: Session = Depends(get_db),
                        user: UserDB = Depends(current_user)):
    db_c = _own_or_404(db, ContributionDB, cid, user.id)
    db.delete(db_c); db.commit()
    return {"ok": True}


# ─── Strengths ───────────────────────────────────────────────────────────────

@app.get("/api/strengths", response_model=List[StrengthOut])
def list_strengths(db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    return db.scalars(
        select(StrengthDB).where(StrengthDB.user_id == user.id).order_by(StrengthDB.created_at.desc())
    ).all()


@app.post("/api/strengths", response_model=StrengthOut, status_code=201)
def create_strength(s: StrengthCreate, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_s = StrengthDB(user_id=user.id, **s.model_dump())
    db.add(db_s); db.commit(); db.refresh(db_s)
    return db_s


@app.put("/api/strengths/{sid}", response_model=StrengthOut)
def update_strength(sid: int, s: StrengthCreate, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_s = _own_or_404(db, StrengthDB, sid, user.id)
    for k, v in s.model_dump().items():
        setattr(db_s, k, v)
    db.commit(); db.refresh(db_s)
    return db_s


@app.delete("/api/strengths/{sid}")
def delete_strength(sid: int, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_s = _own_or_404(db, StrengthDB, sid, user.id)
    db.delete(db_s); db.commit()
    return {"ok": True}


# ─── Priorities ──────────────────────────────────────────────────────────────

@app.get("/api/priorities", response_model=List[PriorityOut])
def list_priorities(db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    return db.scalars(
        select(PriorityDB).where(PriorityDB.user_id == user.id).order_by(PriorityDB.created_at.desc())
    ).all()


@app.post("/api/priorities", response_model=PriorityOut, status_code=201)
def create_priority(p: PriorityCreate, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_p = PriorityDB(user_id=user.id, **p.model_dump())
    db.add(db_p); db.commit(); db.refresh(db_p)
    return db_p


@app.put("/api/priorities/{pid}", response_model=PriorityOut)
def update_priority(pid: int, p: PriorityUpdate, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_p = _own_or_404(db, PriorityDB, pid, user.id)
    for k, v in p.model_dump(exclude_none=True).items():
        setattr(db_p, k, v)
    db.commit(); db.refresh(db_p)
    return db_p


@app.delete("/api/priorities/{pid}")
def delete_priority(pid: int, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_p = _own_or_404(db, PriorityDB, pid, user.id)
    db.delete(db_p); db.commit()
    return {"ok": True}


# ─── Decisions ───────────────────────────────────────────────────────────────

@app.get("/api/decisions", response_model=List[DecisionOut])
def list_decisions(db: Session = Depends(get_db), user: UserDB = Depends(current_user)):
    return db.scalars(
        select(DecisionDB).where(DecisionDB.user_id == user.id).order_by(DecisionDB.created_at.desc())
    ).all()


@app.post("/api/decisions", response_model=DecisionOut, status_code=201)
def create_decision(d: DecisionCreate, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_d = DecisionDB(user_id=user.id, **d.model_dump())
    db.add(db_d); db.commit(); db.refresh(db_d)
    return db_d


@app.put("/api/decisions/{did}", response_model=DecisionOut)
def update_decision(did: int, d: DecisionUpdate, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_d = _own_or_404(db, DecisionDB, did, user.id)
    for k, v in d.model_dump(exclude_none=True).items():
        setattr(db_d, k, v)
    db.commit(); db.refresh(db_d)
    return db_d


@app.delete("/api/decisions/{did}")
def delete_decision(did: int, db: Session = Depends(get_db),
                    user: UserDB = Depends(current_user)):
    db_d = _own_or_404(db, DecisionDB, did, user.id)
    db.delete(db_d); db.commit()
    return {"ok": True}


# ─── Dashboard ───────────────────────────────────────────────────────────────

@app.get("/api/dashboard")
def dashboard(user_id: Optional[int] = None,
              db: Session = Depends(get_db),
              user: UserDB = Depends(current_user)):
    target_id = user_id if user_id is not None else user.id
    if target_id != user.id:
        _assert_manager_can_view(db, user, target_id)

    time_entries = db.scalars(select(TimeEntryDB).where(TimeEntryDB.user_id == target_id)).all()
    contributions = db.scalars(select(ContributionDB).where(ContributionDB.user_id == target_id)).all()
    priorities = db.scalars(select(PriorityDB).where(PriorityDB.user_id == target_id)).all()
    decisions = db.scalars(select(DecisionDB).where(DecisionDB.user_id == target_id)).all()

    by_cat: dict = {}
    for e in time_entries:
        by_cat[e.category] = by_cat.get(e.category, 0) + e.duration_minutes

    target = db.get(UserDB, target_id)
    return {
        "user": {"id": target.id, "email": target.email, "display_name": target.display_name} if target else None,
        "is_self": target_id == user.id,
        "time": {
            "total_hours": round(sum(e.duration_minutes for e in time_entries) / 60, 1),
            "total_entries": len(time_entries),
            "undiagnosed": sum(1 for e in time_entries if e.worth_doing is None),
            "by_category": by_cat,
        },
        "contributions": {
            "total": len(contributions),
            "planned": sum(1 for c in contributions if c.status == "planned"),
            "active": sum(1 for c in contributions if c.status == "active"),
            "completed": sum(1 for c in contributions if c.status == "completed"),
        },
        "priorities": {
            "total": len(priorities),
            "active": sum(1 for p in priorities if p.status == "active"),
            "to_abandon": sum(1 for p in priorities if p.status == "active" and p.would_start_today is False),
        },
        "decisions": {
            "total": len(decisions),
            "open": sum(1 for d in decisions if d.status == "open"),
            "implemented": sum(1 for d in decisions if d.status == "implemented"),
        },
    }


# ─── Static files ────────────────────────────────────────────────────────────

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


@app.exception_handler(HTTPException)
def _http_exc_handler(_request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
