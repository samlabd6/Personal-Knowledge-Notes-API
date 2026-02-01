from fastapi import FastAPI, HTTPException, Depends, Query  
from schemas import PostCreate
from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
from typing import Annotated, Optional, List
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False, unique=True)
    email: Optional[str] = Field(default=None, unique=True)
    password_hash: str = Field(nullable=False)

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    # relationship
    notes: List["Note"] = Relationship(back_populates="user")


class Note(SQLModel, table=True):
    __tablename__ = "notes"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)

    title: str = Field(nullable=False)
    context: Optional[str] = None

    created_at: datetime = Field(
        default_factory=datetime.utcnow
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
        yield Session

SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()

@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit: 
        return list(notes.values())[:limit]
    return notes 

@app.get("/posts/{id}")
def get_post(id: int):
    if id not in notes:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return notes.get(id)


@app.post("/posts")                  # This section below requires that the function only recieves of the PostCreate Schema - and not allow the return of other schema
def create_post(post: PostCreate) -> PostCreate: # fastapi knows automatically that we are recieving a request-body because of pedantic
    new_notice = {"title": post.title, "content": post.content} 
    notes[max(notes.keys()) + 1] = new_notice 
    return new_notice   # because we specified the schema with "-> PostCreate " we can only return that format specified in our schema. 

@app.put("/posts/{id}")
def update_post(id: int):
    pass

@app.delete("/posts/{id}")
def delete_post(id: int):
    pass