import enum
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Date, Enum
from .database import Base
from datetime import datetime
from sqlalchemy.orm import relationship


class StatusEnum(str, enum.Enum):
    pending = "в ожидании"
    in_progress = "в работе"
    done = "выполнено"

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(Date)
    ate_completed = Column(Date, nullable=True)
    equipment = Column(String)
    fault_type = Column(String)
    description = Column(String)
    client = Column(String)
    status = Column(Enum(StatusEnum))
    problem_description = Column(String)
    responsible = Column(String)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(Integer, ForeignKey("requests.id"))
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("Request", back_populates="comments")
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String) 

    requests = relationship("Request", back_populates="owner") 
