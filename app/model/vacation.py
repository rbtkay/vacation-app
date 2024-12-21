import sqlalchemy as sa
from .base import BaseModel
from .base import CustomUUID
from sqlalchemy.orm import relationship


class VacationModel(BaseModel):
    __tablename__ = "vacation"
    start_date = sa.Column(sa.DATE)
    end_date = sa.Column(sa.DATE)

    employee_id = sa.Column(CustomUUID, sa.ForeignKey("employee.id"))  # Foreign key to Employee table
    
    # Relationship back to EmployeeModel
    employee = relationship("EmployeeModel", back_populates="vacations")


