from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

filename = "notes.db"
DATABASE_URL = f"sqlite:///{filename}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionDep = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionDep()
    try:
        yield db
    finally:
        db.close()