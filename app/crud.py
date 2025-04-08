from sqlalchemy.orm import Session
from . import models, schemas

def create_request(db: Session, request: schemas.RequestCreate):
    db_request = models.Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

def get_requests(db: Session):
    return db.query(models.Request).all()
