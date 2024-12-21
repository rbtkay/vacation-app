from app.model import EmployeeModel
from app.repository.base import BaseRepository


class _EmployeeRepository(BaseRepository):
    def get_by_id(self, session, employee_id) -> EmployeeModel:
        return self._query(session, employee_id).first()
    
    def create(self, session, first_name, last_name) -> EmployeeModel:
        return super().create(
            session,
            EmployeeModel(
                first_name=first_name,
                last_name=last_name
            )
        )

EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
