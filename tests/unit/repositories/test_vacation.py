import uuid
from datetime import date
from datetime import timedelta

from app.repository.vacation import VacationRepository
from app.repository.employee import EmployeeRepository


class TestVacationRepository:
    def setup_method(self):
        today = date.today()
        self.start_date = today
        self.end_date = self.start_date + timedelta(days=3)

        self.start_date_later = today + timedelta(days=15)
        self.end_date_later = self.start_date_later + timedelta(days=10)

    def test_get_vacation_by_id_returns_none(self, session):
        vacation = VacationRepository.get_by_id(session, vacation_id=uuid.uuid4())

        assert vacation == None

    def test_create_vacation_success(self, session):
        employee = EmployeeRepository.get(session)

        new_vacation = VacationRepository.create(
            session,
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee
        )

        assert new_vacation.id == new_vacation.id
        assert new_vacation.start_date == self.start_date
        assert new_vacation.end_date == self.end_date
        assert new_vacation.employee == employee
    
    def test_update_vacation_success(self, session):
        employee = EmployeeRepository.get(session)

        new_vacation = VacationRepository.create(
            session,
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee
        )
        assert new_vacation.id == new_vacation.id
        assert new_vacation.start_date == self.start_date
        assert new_vacation.end_date == self.end_date
        assert new_vacation.employee == employee

        result = VacationRepository.update(session, new_vacation.id, self.start_date_later, self.end_date_later)
        assert result == 1

        updated_vacation = VacationRepository.get_by_id(session, vacation_id=new_vacation.id)
        
        assert updated_vacation.id == new_vacation.id
        assert updated_vacation.start_date == self.start_date_later
        assert updated_vacation.end_date == self.end_date_later
        assert updated_vacation.employee == employee

    def test_cant_update_vacation_if_not_found(self, session):
        result = VacationRepository.update(session, uuid.uuid4(), self.start_date_later, self.end_date_later)

        assert result == 0

    def test_delete_vacation_success(self, session):
        employee = EmployeeRepository.get(session)

        new_vacation = VacationRepository.create(
            session,
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee
        )
        result = VacationRepository.delete(session, new_vacation.id)
        assert result == 1
        
        vacation = VacationRepository.get_by_id(session, new_vacation.id)
        assert vacation is None

