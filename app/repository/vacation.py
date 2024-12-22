from app.model import VacationModel
from app.model.employee import EmployeeModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository):
    def get_by_id(self, session, vacation_id) -> VacationModel:
        return self._query(session, id=vacation_id).first()
    
    def validate_dates(self, start_date, end_date):
        if start_date > end_date:
            raise ValueError("start_date should be before the end_date")
    
    def validate_overlapping_vacation(self, session, start_date, end_date, vacation_type, employee: EmployeeModel):
        overlapping_vacation = session.query(self.model).filter(
            VacationModel.employee_id == employee.id,
            VacationModel.end_date >= start_date,
            VacationModel.start_date <= end_date,
            VacationModel.vacation_type != vacation_type
        ).first()

        if overlapping_vacation:
            raise ValueError("There is already an overlapping vacation with a different type during this date range.")

    def create(self, session, start_date, end_date, vacation_type, employee: EmployeeModel) -> VacationModel:
        self.validate_dates(start_date, end_date)
        self.validate_overlapping_vacation(session, start_date, end_date, vacation_type, employee)

        return super().create(
            session,
            VacationModel(
                start_date=start_date,
                end_date=end_date,
                employee=employee,
                vacation_type=vacation_type
            )
        )

    def update(self, session, vacation_id, start_date, end_date, vacation_type) -> int:
        self.validate_dates(start_date, end_date)

        return self._query(
            session,
            id=vacation_id,
        ).update({
            "start_date": start_date,
            "end_date": end_date,
            "vacation_type": vacation_type
        })
    
    def merge(self, session, employee_id, start_date, end_date, vacation_type) -> int:
        self.validate_dates(start_date, end_date)

        statement = self._query(
            session,
            employee_id=employee_id,
            vacation_type=vacation_type
        )
        result = statement.filter(
            self.model.start_date >= start_date
        ).filter(self.model.start_date <= end_date).update({"start_date": start_date})
        
        result += statement.filter(
            self.model.end_date >= start_date
        ).filter(self.model.end_date <= end_date).update({"end_date": end_date})

        return result

    def delete(self, session, vacation_id) -> int:
        return self._query(session, id=vacation_id).delete()


VacationRepository = _VacationRepository(model=VacationModel)
