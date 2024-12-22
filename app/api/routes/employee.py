from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    Query
)
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository
from app.schema import EmployeeBase
from app.schema import VacationBase

router = APIRouter()


@router.get("/off", response_model=Optional[list[EmployeeBase]])
def get_employees_in_vacation(
    requested_date: str,
    session: Session = Depends(get_db),
    first_name: str = Query(None, min_length=3, description="Filter employees by first name"),
    last_name: str = Query(None, min_length=3, description="Filter employees by last name"),
):
    return EmployeeRepository.get_in_vacation(
        session,
        requested_date,
        first_name, 
        last_name, 
    )

@router.get("/{employee_id}/vacations", response_model=Optional[list[VacationBase]])
def get_vacations(session: Session = Depends(get_db), *, employee_id: UUID):
    result = VacationRepository.get_many(session=session, employee_id=employee_id)

    return result


@router.get("/{employee_id}", response_model=Optional[EmployeeBase])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):

    breakpoint()
    return EmployeeRepository.get(session=session, id=employee_id)


@router.get("/", response_model=Optional[list[EmployeeBase]])
def get_employees(session: Session = Depends(get_db)):
    return EmployeeRepository.get_many(session=session)


@router.post("/")
def create_employee(payload: EmployeeBase, session: Session = Depends(get_db)):

    breakpoint()
    return EmployeeRepository.create(
        session=session,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
