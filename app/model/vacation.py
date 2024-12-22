import sqlalchemy as sa
from .base import BaseModel
from .base import CustomUUID
from sqlalchemy.orm import relationship
from app.enum.vacation import ALLOWED_VACATION_TYPE


class VacationModel(BaseModel):
    __tablename__ = "vacation"
    start_date = sa.Column(sa.DATE, nullable=False)
    end_date = sa.Column(sa.DATE, nullable=False)

    vacation_type = sa.Column(sa.String, nullable=False)

    employee_id = sa.Column(CustomUUID, sa.ForeignKey("employee.id"))
    employee = relationship("EmployeeModel", back_populates="vacations")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.vacation_type not in ALLOWED_VACATION_TYPE:
            raise ValueError(f"vacation_type must be 'paid leave' or 'unpaid leave', got {self.vacation_type}")


