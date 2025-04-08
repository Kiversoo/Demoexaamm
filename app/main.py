from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
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

@app.post("/requests/", response_model=schemas.Request)
def create_request(request: schemas.RequestCreate, db: Session = Depends(get_db)):
    return crud.create_request(db, request)

@app.get("/requests/", response_model=list[schemas.Request])
def read_requests(db: Session = Depends(get_db)):
    return crud.get_requests(db)

@app.put("/requests/{request_id}/status", response_model=schemas.RequestUpdate)
def update_status(request_id: int, status: schemas.Status, db: Session = Depends(get_db)):
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