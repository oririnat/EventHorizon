# schemas.py

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ActorSchema(BaseModel):
    id: int
    login: str
    avatar_url: Optional[str] = None

    class Config:
        orm_mode = True

class RepositorySchema(BaseModel):
    id: int
    name: str
    stars: Optional[int] = None

    class Config:
        orm_mode = True

class EventSchema(BaseModel):
    id: str
    type: str
    actor: ActorSchema  
    repository: RepositorySchema
    created_at: datetime

    class Config:
        orm_mode = True
