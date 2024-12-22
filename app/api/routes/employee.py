from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    Query
)
from sqlalchemy.orm import Session
from fastapi import status

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository
from app.schema import EmployeeBase
from app.schema import EmployeeGetSchema
from app.schema import VacationBase

router = APIRouter()


@router.get("/off/{requested_date}", response_model=Optional[list[EmployeeGetSchema]])
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
    employee = EmployeeRepository.get(session, id=employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} does not exist"
        )
    
    result = VacationRepository.get_many(session=session, employee_id=employee_id)

    return result


@router.get("/{employee_id}", response_model=Optional[EmployeeGetSchema])
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    employee = EmployeeRepository.get(session=session, id=employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {employee_id} does not exist"
        )

    return employee
    

@router.get("/", response_model=Optional[list[EmployeeGetSchema]])
def get_employees(session: Session = Depends(get_db)):
    return EmployeeRepository.get_many(session=session)


@router.post("/", response_model=EmployeeGetSchema, status_code=status.HTTP_201_CREATED)
def create_employee(payload: EmployeeBase, session: Session = Depends(get_db)):
    return EmployeeRepository.create(
        session=session,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
