from fastapi import FastAPI, HTTPException, Depends
from schemas import Users, Notes
from datetime import date
from pydantic import BaseModel
from database import get_db, Base, SessionDep
from models import User, Note
from sqlalchemy import Session

@app.get("/notices")
def get_all_posts(db: Session = Depends(get_db)):
    notices = Note
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