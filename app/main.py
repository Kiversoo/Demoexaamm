from pickle import APPEND
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi import security
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from typing import List
from app.routers import tasks 
from . import models, schemas, crud
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(tasks.router)

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

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# регестрация енового пользователя 
@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(SessionLocal)):
    hashed_password = security.hash_password(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role="user")
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# логин 
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(SessionLocal)):
    db_user = crud.get_user_by_username(db, username=form_data.username)
    if not db_user or not security.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = security.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = security.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return current_user

# ограничения для разных пользователй 
@router.get("/admin-only", dependencies=[Depends(get_current_admin_user)])
def admin_only_route():
    return {"message": "Welcome, admin!"}

@router.get("/user-only")
def user_only_route(current_user: dict = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user['sub']}!"}
