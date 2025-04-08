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

def update_status(db: Session, request_id: int, status: str):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request:
        db_request.status = status
        db.commit()  
        db.refresh(db_request) 
    return db_request


def update_problem_description(db: Session, request_id: int, problem_description: str):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request:
        db_request.problem_description = problem_description
        db.commit()
        db.refresh(db_request)
    return db_request


def update_responsible(db: Session, request_id: int, responsible: str):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if db_request:
        db_request.responsible = responsible
        db.commit()
        db.refresh(db_request)
    return db_request