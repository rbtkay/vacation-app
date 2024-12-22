from app.model import VacationModel
from app.model.employee import EmployeeModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository):
    def get_by_id(self, session, vacation_id) -> VacationModel:
        return self._query(session, id=vacation_id).first()
    
    def validate_dates(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError("start_date should be before the end_date")

    def create(self, session, start_date, end_date, employee: EmployeeModel) -> VacationModel:
        self.validate_dates(start_date, end_date)

        return super().create(
            session,
            VacationModel(
                start_date=start_date,
                end_date=end_date,
                employee=employee,
            )
        )

    def update(self, session, vacation_id, start_date, end_date) -> int:
        self.validate_dates(start_date, end_date)

        return self._query(
            session,
            id=vacation_id,
        ).update({"start_date": start_date, "end_date": end_date})
    
    def merge(self, session, employee_id, start_date, end_date) -> int:
        self.validate_dates(start_date, end_date)

        statement = self._query(
            session,
            employee_id=employee_id,
        )
        result = statement.filter(
            self.model.start_date > start_date
        ).filter(self.model.start_date <= end_date).update({"start_date": start_date})
        
        result += statement.filter(
            self.model.end_date >= start_date
        ).filter(self.model.end_date < end_date).update({"end_date": end_date})

        return result

    def delete(self, session, vacation_id) -> int:
        return self._query(session, id=vacation_id).delete()


VacationRepository = _VacationRepository(model=VacationModel)
