import enum
from sqlalchemy import Column, Integer, String, Date, Enum
from .database import Base

class StatusEnum(str, enum.Enum):
    pending = "в ожидании"
    in_progress = "в работе"
    done = "выполнено"

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(Date)
    equipment = Column(String)
    fault_type = Column(String)
    description = Column(String)
    client = Column(String)
    status = Column(Enum(StatusEnum))
