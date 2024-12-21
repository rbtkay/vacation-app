from pydantic import BaseModel, ConfigDict, field_validator
from datetime import date
from app.schema import EmployeeBase
from uuid import UUID


class VacationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    start_date: date
    end_date: date

    employee: EmployeeBase



class VacationPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_date: str
    end_date: str
    employee_id: UUID

    @field_validator("start_date")
    def validate_start_date(cls, value):
        try:
            print(value)
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid date format, must be YYYY-MM-DD")


    @field_validator("end_date")
    def validate_end_date(cls, value):
        try:
            return date.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid date format, must be YYYY-MM-DD")

class VacationUpdatePayload(VacationPayload):
    id: UUID
