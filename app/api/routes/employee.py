from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema import EmployeeBase

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[EmployeeBase])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    return EmployeeRepository.get(session=session, id=employee_id)


@router.post("/")
def create_employee(payload: EmployeeBase, session: Session = Depends(get_db)):
    return EmployeeRepository.create(
        session=session,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
