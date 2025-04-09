from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/requests/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db, request)

@app.get("/requests/", response_model=list[schemas.Request])
def read_requests(db: Session = Depends(get_db)):
    return crud.get_requests(db)

@app.put("/requests/{request_id}/status", response_model=schemas.RequestUpdate)
def update_status(request_id: int, status: schemas.StatusEnum, db: Session = Depends(get_db)):
    db_request = crud.update_status(db=db, request_id=request_id, status=status)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request


@app.put("/requests/{request_id}/problem_description", response_model=schemas.RequestUpdate)
def update_problem_description(request_id: int, problem_description: str, db: Session = Depends(get_db)):
    db_request = crud.update_problem_description(db=db, request_id=request_id, problem_description=problem_description)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request


@app.put("/requests/{request_id}/responsible", response_model=schemas.RequestUpdate)
def update_responsible(request_id: int, responsible: str, db: Session = Depends(get_db)):
    db_request = crud.update_responsible(db=db, request_id=request_id, responsible=responsible)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@app.get("/requests", response_model=List[schemas.Request])
def get_requests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    requests = crud.get_requests(db=db, skip=skip, limit=limit)
    return requests

@app.put("/requests/{request_id}", response_model=schemas.Request)
def update_request(request_id: int, status: schemas.StatusEnum, responsible: str = None, problem_description: str = None, db: Session = Depends(get_db)):
    return crud.update_request_status(db=db, request_id=request_id, status=status, responsible=responsible, problem_description=problem_description)

@app.get("/requests/search", response_model=List[schemas.Request])
def search_requests(request_id: int = None, client: str = None, equipment: str = None, db: Session = Depends(get_db)):
    return crud.search_requests(db=db, request_id=request_id, client=client, equipment=equipment)

@app.put("/requests/{request_id}", response_model=schemas.Request)
def update_request(request_id: int, status: schemas.StatusEnum, responsible: str = None, problem_description: str = None, db: Session = Depends(get_db)):
    return crud.update_request_status(db=db, request_id=request_id, status=status, responsible=responsible, problem_description=problem_description)

@app.put("/requests/{request_id}/complete", response_model=schemas.Request)
def complete_request(request_id: int, db: Session = Depends(get_db)):
    return crud.complete_request(db=db, request_id=request_id)

@app.post("/requests/{request_id}/comments", response_model=schemas.Comment)
def create_comment(request_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, request_id=request_id, comment=comment)

@app.get("/tasks/completed")
def get_completed_tasks(db: Session = Depends(get_db)):
    completed_tasks = crud.count_completed_tasks(db)
    return {"completed_tasks": completed_tasks}

@app.get("/tasks/average_completion_time")
def get_average_completion_time(db: Session = Depends(get_db)):
    avg_time = crud.average_completion_time(db)
    return {"average_completion_time": avg_time}

@app.get("/tasks/fault_type_statistics")
def get_fault_type_statistics(db: Session = Depends(get_db)):
    statistics = crud.fault_type_statistics(db)
    return {"fault_type_statistics": statistics}
