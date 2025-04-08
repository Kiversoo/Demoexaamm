from fastapi import HTTPException
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

def get_requests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Request).offset(skip).limit(limit).all()

def update_request_status(db: Session, request_id: int, status: str, responsible: str | None = None, problem_description: str | None = None):
    db_request = db.query(models.Request).filter(models.Request.id == request_id).first()
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")

    db_request.status = status
    
    if responsible:
        db_request.responsible = responsible
    if problem_description:
        db_request.description = problem_description

    db.commit()
    db.refresh(db_request)

    print(f"Заявка {request_id} изменена. Новый статус: {status}")

    return db_request

def search_requests(db: Session, request_id: int = None, client: str = None, equipment: str = None):
    query = db.query(models.Request)

    if request_id:
        query = query.filter(models.Request.id == request_id)
    if client:
        query = query.filter(models.Request.client == client)
    if equipment:
        query = query.filter(models.Request.equipment == equipment)

    return query.all()
