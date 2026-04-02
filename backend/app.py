from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db, engine
from tables import Base, Note, User
from schemas import NoteCreate, NoteResponse, UserCreate, UserLogin, UserResponse

from encryp import hash_password, verify_password

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/notices", response_model=list[NoteResponse])
def get_all_posts(db: Session = Depends(get_db)):
    return db.query(Note).all()

@app.get("/notices/{id}", response_model=NoteResponse)
def get_post(id: int, db: Session = Depends(get_db) ):
    notice = db.get(Note, id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return notice


@app.post("/notices", response_model=NoteResponse)                 
def create_notice(notice: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(**notice.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.put("/posts/{id}") 
def update_post(id: int):
    pass

@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    notice = db.get(Note, id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    db.delete(notice)
    db.commit()
    return {"message": "Notice deleted successfully"}


@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_pw[1], salt=hashed_pw[0])
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")

@app.post("/login", response_model=UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first() 
    
    if not db_user or not verify_password(db_user.salt, db_user.password_hash, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return db_user