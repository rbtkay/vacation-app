from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
    HTTPException
)
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repository.vacation import VacationRepository
from app.repository.employee import EmployeeRepository
from app.schema import VacationBase
from app.schema import VacationPayload
from app.schema import VacationUpdatePayload

router = APIRouter()


@router.get("/{vacation_id}", response_model=Optional[VacationBase])
def get_vacation(session: Session = Depends(get_db), *, vacation_id: UUID):
    vacation = VacationRepository.get(session=session, id=vacation_id)
    if vacation is None:
        raise HTTPException(status_code=404, detail="Vacation not found")
    
    return vacation


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vacation(payload: VacationPayload, session: Session = Depends(get_db)):
    employee = EmployeeRepository.get(session, id=payload.employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {payload.employee_id} does not exist"
        )
    
    if VacationRepository.merge(session, employee.id, payload.start_date, payload.end_date) <= 0:
        VacationRepository.create(
            session,
            payload.start_date,
            payload.end_date,
            employee=employee,
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Vacation created successfully"
        }
    )


@router.put("/", status_code=status.HTTP_201_CREATED)
def update_vacation(payload: VacationUpdatePayload, session: Session = Depends(get_db)):
    employee = EmployeeRepository.get(session, id=payload.employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id {payload.employee_id} does not exist"
        )
    
    result = VacationRepository.update(
        session,
        payload.id,
        payload.start_date,
        payload.end_date,
    )

    if result <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vacation with id {payload.employee_id} does not exist"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Vacation {payload.id} was updated successfully"
        }
    )


@router.delete("/{vacation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacation(vacation_id: UUID, session: Session = Depends(get_db)):
    VacationRepository.delete(session, vacation_id)

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": f"Vacation {vacation_id} was deleted successfully"}
    )
