from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository
from app.schema import EmployeeBase
from app.schema import VacationBase

router = APIRouter()


@router.get("/{employee_id}", response_model=Optional[EmployeeBase])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    return EmployeeRepository.get(session=session, id=employee_id)


@router.get("/", response_model=Optional[list[EmployeeBase]])
def get_employees(session: Session = Depends(get_db)):
    return EmployeeRepository.get_many(session=session)


@router.post("/")
def create_employee(payload: EmployeeBase, session: Session = Depends(get_db)):
    return EmployeeRepository.create(
        session=session,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )


@router.get("/{employee_id}/vacations", response_model=Optional[list[VacationBase]])
def get_vacations(session: Session = Depends(get_db), *, employee_id: UUID):
    result = VacationRepository.get_many(session=session, employee_id=employee_id)

    return result


@router.get("/{employee_id}/off", response_model=Optional[list[VacationBase]])
def get_employee_in_vacation(session: Session = Depends(get_db)):
    pass