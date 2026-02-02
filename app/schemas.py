from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    context: str
    user_id: int


class NoteResponse(BaseModel):
    id: int
    title: str
    context: str
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True
