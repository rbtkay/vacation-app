from app.model import EmployeeModel
from app.model import VacationModel
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

    def get_in_vacation(
        self,
        session,
        requested_date,
        first_name = None,
        last_name = None,
    ) -> EmployeeModel:
        statement = session.query(self.model).join(VacationModel)

        if first_name:
            statement = statement.filter(EmployeeModel.first_name == first_name)
        if last_name:
            statement = statement.filter(EmployeeModel.last_name == last_name)
        if requested_date:
            statement = statement.filter(
                VacationModel.start_date < requested_date
            ).filter(
                VacationModel.end_date > requested_date
            )

        return statement.all()
        
EmployeeRepository = _EmployeeRepository(model=EmployeeModel)
