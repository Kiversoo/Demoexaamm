from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum

class StatusEnum(str, Enum):
    pending = "в ожидании"
    in_progress = "в работе"
    done = "выполнено"

class RequestCreate(BaseModel):
    date_created: date
    equipment: str
    fault_type: str
    description: str
    client: str
    status: StatusEnum
    responsible: str

class Request(RequestCreate):
    id: int

    class Config:
        orm_mode = True

class RequestUpdate(BaseModel):
    status: StatusEnum | None = None  
    problem_description: str | None = None  
    responsible: str | None = None  

    class Config:
        orm_mode = True  

class CommentCreate(BaseModel):
    text: str

class Comment(CommentCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

