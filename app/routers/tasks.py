from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud
from app.database import get_db


router = APIRouter(
    prefix="/tasks",  
    tags=["tasks"],  
)

@router.get("/completed")
def get_completed_tasks(db: Session = Depends(get_db)):
    completed_tasks = crud.count_completed_tasks(db)
    return {"completed_tasks": completed_tasks}


@router.get("/average_completion_time")
def get_average_completion_time(db: Session = Depends(get_db)):
    avg_time = crud.average_completion_time(db)
    return {"average_completion_time": avg_time}


@router.get("/fault_type_statistics")
def get_fault_type_statistics(db: Session = Depends(get_db)):
    statistics = crud.fault_type_statistics(db)
    return {"fault_type_statistics": statistics}
