from sqlalchemy import Column, Integer, String, Date
from database import Base

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(Date, nullable=True)
    notes = Column # to do - foriegn key