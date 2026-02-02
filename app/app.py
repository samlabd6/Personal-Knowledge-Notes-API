from fastapi import FastAPI, HTTPException, Depends, Query  
from schemas import PostCreate
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from typing import Annotated, Optional, List
from datetime import datetime
from contextlib import asynccontextmanager 

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: Optional[str] = Field(default=None, unique=True)
    password_hash: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    notes: List["Note"] = Relationship(back_populates="user")


class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)

    title: str = Field(nullable=False)
    context: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    is_archived: bool = Field(default=False)

    user: Optional[User] = Relationship(back_populates="notes")

filename = "notes.db"
DATABASE_URL = f"sqlite:///{filename}"

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session: 
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI): 
    create_db_and_tables()


app = FastAPI(lifespan=lifespan)

@app.get("/notices")
def get_all_posts(session: SessionDep, 
                  offset: int = 0, 
                  limit: Annotated[int, Query(le=100)] = 100) -> list[Note]:
    notices = session.exec(select(Note).offset(offset).limit(limit)).all()
    return notices


@app.get("/notices/{id}")
def get_post(id: int, session: SessionDep) -> Note:
    notice = session.get(Note, id)
    if not Note:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice


@app.post("/notices")                 
def create_notice(notice: Note, session: SessionDep) -> Note:
    session.add(notice)
    session.commit()
    session.refresh(notice)
    return notice


@app.put("/posts/{id}")
def update_post(id: int):
    pass

@app.delete("/posts/{id}")
def delete_post(id: int, session: SessionDep):
    notice = session.get(Note, id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    session.delete(notice)
    session.commit()
    return {"ok": True}