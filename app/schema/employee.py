from pydantic import BaseModel, ConfigDict
from uuid import UUID


class EmployeeBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str

class EmployeeGetSchema(EmployeeBase):
    id: UUID
