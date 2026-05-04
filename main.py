from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import os

DATABASE_URL = "sqlite:///./effective_executive.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# --- ORM Models ---

class TimeEntryDB(Base):
    __tablename__ = "time_entries"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    activity = Column(String(500), nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    # deep_work | meeting | admin | communication | waste | uncategorized
    category = Column(String(50), default="uncategorized")
    # Drucker's three diagnostic questions
    worth_doing = Column(Boolean, nullable=True)   # None = undiagnosed
    can_delegate = Column(Boolean, nullable=True)
    wastes_others = Column(Boolean, nullable=True)
    notes = Column(Text, default="")


class ContributionDB(Base):
    __tablename__ = "contributions"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    activity = Column(String(500), nullable=False)
    expected_outcome = Column(Text, default="")
    # direct_results | values | talent
    layer = Column(String(50), default="direct_results")
    actual_outcome = Column(Text, default="")
    # planned | active | completed | cancelled
    status = Column(String(50), default="planned")


class StrengthDB(Base):
    __tablename__ = "strengths"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, default="")
    owner = Column(String(200), default="self")
    evidence = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class PriorityDB(Base):
    __tablename__ = "priorities"
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, default="")
    future_oriented = Column(Boolean, default=False)
    opportunity_not_problem = Column(Boolean, default=False)
    own_direction = Column(Boolean, default=False)
    high_meaning = Column(Boolean, default=False)
    would_start_today = Column(Boolean, nullable=True)  # None = not reviewed
    # active | abandoned | done
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class DecisionDB(Base):
    __tablename__ = "decisions"
    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    # generic | unique
    problem_type = Column(String(50), default="generic")
    boundary_conditions = Column(Text, default="")
    right_answer = Column(Text, default="")
    compromise = Column(Text, default="")
    assignee = Column(String(200), default="")
    feedback_mechanism = Column(Text, default="")
    has_dissent = Column(Boolean, default=False)
    # open | implemented | reviewed
    status = Column(String(50), default="open")
    outcome = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


# --- Pydantic Schemas ---

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


# --- App ---

app = FastAPI(title="The Effective Executive")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Time Entries ---

@app.get("/api/time-entries/analysis")
def analyze_time(db: Session = Depends(get_db)):
    entries = db.query(TimeEntryDB).all()
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
def list_time_entries(db: Session = Depends(get_db)):
    return db.query(TimeEntryDB).order_by(TimeEntryDB.timestamp.desc()).all()


@app.post("/api/time-entries", response_model=TimeEntryOut, status_code=201)
def create_time_entry(entry: TimeEntryCreate, db: Session = Depends(get_db)):
    db_e = TimeEntryDB(**entry.model_dump())
    db.add(db_e)
    db.commit()
    db.refresh(db_e)
    return db_e


@app.put("/api/time-entries/{entry_id}", response_model=TimeEntryOut)
def update_time_entry(entry_id: int, entry: TimeEntryUpdate, db: Session = Depends(get_db)):
    db_e = db.query(TimeEntryDB).filter(TimeEntryDB.id == entry_id).first()
    if not db_e:
        raise HTTPException(404, "Not found")
    for k, v in entry.model_dump(exclude_none=True).items():
        setattr(db_e, k, v)
    db.commit()
    db.refresh(db_e)
    return db_e


@app.delete("/api/time-entries/{entry_id}")
def delete_time_entry(entry_id: int, db: Session = Depends(get_db)):
    db_e = db.query(TimeEntryDB).filter(TimeEntryDB.id == entry_id).first()
    if not db_e:
        raise HTTPException(404, "Not found")
    db.delete(db_e)
    db.commit()
    return {"ok": True}


# --- Contributions ---

@app.get("/api/contributions", response_model=List[ContributionOut])
def list_contributions(db: Session = Depends(get_db)):
    return db.query(ContributionDB).order_by(ContributionDB.created_at.desc()).all()


@app.post("/api/contributions", response_model=ContributionOut, status_code=201)
def create_contribution(c: ContributionCreate, db: Session = Depends(get_db)):
    db_c = ContributionDB(**c.model_dump())
    db.add(db_c)
    db.commit()
    db.refresh(db_c)
    return db_c


@app.put("/api/contributions/{cid}", response_model=ContributionOut)
def update_contribution(cid: int, c: ContributionUpdate, db: Session = Depends(get_db)):
    db_c = db.query(ContributionDB).filter(ContributionDB.id == cid).first()
    if not db_c:
        raise HTTPException(404, "Not found")
    for k, v in c.model_dump(exclude_none=True).items():
        setattr(db_c, k, v)
    db.commit()
    db.refresh(db_c)
    return db_c


@app.delete("/api/contributions/{cid}")
def delete_contribution(cid: int, db: Session = Depends(get_db)):
    db_c = db.query(ContributionDB).filter(ContributionDB.id == cid).first()
    if not db_c:
        raise HTTPException(404, "Not found")
    db.delete(db_c)
    db.commit()
    return {"ok": True}


# --- Strengths ---

@app.get("/api/strengths", response_model=List[StrengthOut])
def list_strengths(db: Session = Depends(get_db)):
    return db.query(StrengthDB).order_by(StrengthDB.created_at.desc()).all()


@app.post("/api/strengths", response_model=StrengthOut, status_code=201)
def create_strength(s: StrengthCreate, db: Session = Depends(get_db)):
    db_s = StrengthDB(**s.model_dump())
    db.add(db_s)
    db.commit()
    db.refresh(db_s)
    return db_s


@app.put("/api/strengths/{sid}", response_model=StrengthOut)
def update_strength(sid: int, s: StrengthCreate, db: Session = Depends(get_db)):
    db_s = db.query(StrengthDB).filter(StrengthDB.id == sid).first()
    if not db_s:
        raise HTTPException(404, "Not found")
    for k, v in s.model_dump().items():
        setattr(db_s, k, v)
    db.commit()
    db.refresh(db_s)
    return db_s


@app.delete("/api/strengths/{sid}")
def delete_strength(sid: int, db: Session = Depends(get_db)):
    db_s = db.query(StrengthDB).filter(StrengthDB.id == sid).first()
    if not db_s:
        raise HTTPException(404, "Not found")
    db.delete(db_s)
    db.commit()
    return {"ok": True}


# --- Priorities ---

@app.get("/api/priorities", response_model=List[PriorityOut])
def list_priorities(db: Session = Depends(get_db)):
    return db.query(PriorityDB).order_by(PriorityDB.created_at.desc()).all()


@app.post("/api/priorities", response_model=PriorityOut, status_code=201)
def create_priority(p: PriorityCreate, db: Session = Depends(get_db)):
    db_p = PriorityDB(**p.model_dump())
    db.add(db_p)
    db.commit()
    db.refresh(db_p)
    return db_p


@app.put("/api/priorities/{pid}", response_model=PriorityOut)
def update_priority(pid: int, p: PriorityUpdate, db: Session = Depends(get_db)):
    db_p = db.query(PriorityDB).filter(PriorityDB.id == pid).first()
    if not db_p:
        raise HTTPException(404, "Not found")
    for k, v in p.model_dump(exclude_none=True).items():
        setattr(db_p, k, v)
    db.commit()
    db.refresh(db_p)
    return db_p


@app.delete("/api/priorities/{pid}")
def delete_priority(pid: int, db: Session = Depends(get_db)):
    db_p = db.query(PriorityDB).filter(PriorityDB.id == pid).first()
    if not db_p:
        raise HTTPException(404, "Not found")
    db.delete(db_p)
    db.commit()
    return {"ok": True}


# --- Decisions ---

@app.get("/api/decisions", response_model=List[DecisionOut])
def list_decisions(db: Session = Depends(get_db)):
    return db.query(DecisionDB).order_by(DecisionDB.created_at.desc()).all()


@app.post("/api/decisions", response_model=DecisionOut, status_code=201)
def create_decision(d: DecisionCreate, db: Session = Depends(get_db)):
    db_d = DecisionDB(**d.model_dump())
    db.add(db_d)
    db.commit()
    db.refresh(db_d)
    return db_d


@app.put("/api/decisions/{did}", response_model=DecisionOut)
def update_decision(did: int, d: DecisionUpdate, db: Session = Depends(get_db)):
    db_d = db.query(DecisionDB).filter(DecisionDB.id == did).first()
    if not db_d:
        raise HTTPException(404, "Not found")
    for k, v in d.model_dump(exclude_none=True).items():
        setattr(db_d, k, v)
    db.commit()
    db.refresh(db_d)
    return db_d


@app.delete("/api/decisions/{did}")
def delete_decision(did: int, db: Session = Depends(get_db)):
    db_d = db.query(DecisionDB).filter(DecisionDB.id == did).first()
    if not db_d:
        raise HTTPException(404, "Not found")
    db.delete(db_d)
    db.commit()
    return {"ok": True}


# --- Dashboard ---

@app.get("/api/dashboard")
def dashboard(db: Session = Depends(get_db)):
    time_entries = db.query(TimeEntryDB).all()
    contributions = db.query(ContributionDB).all()
    priorities = db.query(PriorityDB).all()
    decisions = db.query(DecisionDB).all()

    by_cat: dict = {}
    for e in time_entries:
        by_cat[e.category] = by_cat.get(e.category, 0) + e.duration_minutes

    return {
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


# --- Static files ---

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def index():
    return FileResponse("static/index.html")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
