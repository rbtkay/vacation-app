from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from datetime import date
from app.schema import EmployeeGetSchema
from uuid import UUID

from app.enum import ALLOWED_VACATION_TYPE


class VacationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    start_date: date
    end_date: date

    employee: EmployeeGetSchema
    vacation_type: str


class VacationPayloadBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_date: date
    end_date: date

    vacation_type: str

    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")
        return self

    @model_validator(mode="after")
    def validate_vacation_type(self):
        if self.vacation_type not in ALLOWED_VACATION_TYPE:
            raise ValueError(f"Vacation type must be in {ALLOWED_VACATION_TYPE}")
        return self
    

class VacationCreatePayload(VacationPayloadBase):
    employee_id: UUID
