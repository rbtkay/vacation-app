from app.model import VacationModel
from app.model.employee import EmployeeModel
from app.repository.base import BaseRepository


class _VacationRepository(BaseRepository):
    def get_by_id(self, session, vacation_id) -> VacationModel:
        return self._query(session, id=vacation_id).first()
    
    def create(self, session, start_date, end_date, employee: EmployeeModel) -> VacationModel:
        return super().create(
            session,
            VacationModel(
                start_date=start_date,
                end_date=end_date,
                employee=employee,
            )
        )

    def update(self, session, vacation_id, start_date, end_date) -> int:
        return self._query(
            session,
            id=vacation_id,
        ).update({"start_date": start_date, "end_date": end_date, })
    

    def delete(self, session, vacation_id) -> int:
        return self._query(session, id=vacation_id).delete()


VacationRepository = _VacationRepository(model=VacationModel)
