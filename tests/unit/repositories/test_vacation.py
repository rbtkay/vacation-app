import uuid
import pytest

from datetime import date
from datetime import timedelta

from app.repository.vacation import VacationRepository

from tests.factories import EmployeeFactory
from tests.factories import VacationFactory

class TestVacationRepository:
    def setup_method(self):
        today = date(2024, 1, 1)
        self.start_date = today
        self.end_date = self.start_date + timedelta(days=3)

        self.start_date_later = today + timedelta(days=15)
        self.end_date_later = self.start_date_later + timedelta(days=10)

    def test_get_vacation_by_id_returns_none(self, session):
        vacation = VacationRepository.get_by_id(session, vacation_id=uuid.uuid4())

        assert vacation == None

    def test_create_vacation_success(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        new_vacation = VacationRepository.create(
            session,
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee,
            vacation_type="paid leave"
        )

        assert new_vacation.id == new_vacation.id
        assert new_vacation.start_date == self.start_date
        assert new_vacation.end_date == self.end_date
        assert new_vacation.employee == employee
    
    def test_create_vacation_raises_if_wrong_dates(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        with pytest.raises(ValueError):
            VacationRepository.create(
                session,
                start_date=self.end_date,
                end_date=self.start_date,
                employee=employee,
                vacation_type="paid leave"
            )
    
    def test_create_vacation_raises_if_wrong_type(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        with pytest.raises(ValueError):
            VacationRepository.create(
                session,
                start_date=self.start_date,
                end_date=self.end_date,
                employee=employee,
                vacation_type="something leave"
            )
    
    def test_create_vacation_raises_if_overlapping_vacation(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )
        VacationFactory(session).create(
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee,
            vacation_type="paid leave"
        )

        with pytest.raises(ValueError):
            VacationRepository.create(
                session,
                start_date=self.start_date - timedelta(days=2),
                end_date=self.end_date,
                employee=employee,
                vacation_type="unpaid leave"
            )
    

    def test_update_vacation_success(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        new_vacation = VacationFactory(session).create(
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee
        )

        result = VacationRepository.update(
            session,
            new_vacation.id,
            self.start_date_later,
            self.end_date_later,
            vacation_type='paid leave',
        )
        assert result == 1

        updated_vacation = VacationRepository.get_by_id(session, vacation_id=new_vacation.id)
        
        assert updated_vacation.id == new_vacation.id
        assert updated_vacation.start_date == self.start_date_later
        assert updated_vacation.end_date == self.end_date_later
        assert updated_vacation.employee == employee
        assert updated_vacation.vacation_type == new_vacation.vacation_type

    def test_cant_update_vacation_if_not_found(self, session):
        result = VacationRepository.update(
            session,
            uuid.uuid4(),
            self.start_date_later,
            self.end_date_later,
            vacation_type='paid leave'
        )

        assert result == 0

    def test_delete_vacation_success(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        new_vacation = VacationFactory(session).create(
            start_date=self.start_date,
            end_date=self.end_date,
            employee=employee
        )
        result = VacationRepository.delete(session, new_vacation.id)
        assert result == 1
        
        vacation = VacationRepository.get_by_id(session, new_vacation.id)
        assert vacation is None
    
    def test_merge_when_start_date_mathches(self, session):
        today = date(2025, 1, 1)
        
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )
        
        vacation = VacationFactory(session).create(
            start_date=today,
            end_date=today + timedelta(days=10),
            employee=employee,
        )

        new_start_date = vacation.start_date - timedelta(days=5)
        new_end_date = vacation.start_date + timedelta(days=5)
        
        result = VacationRepository.merge(
            session,
            employee_id=vacation.employee.id,
            start_date=new_start_date,
            end_date=new_end_date,
            vacation_type=vacation.vacation_type
        )

        assert result == 1
        
        updated_vacation = VacationRepository.get_by_id(session, vacation_id=vacation.id)
        assert updated_vacation.start_date == new_start_date
        assert updated_vacation.end_date == vacation.end_date

    def test_merge_when_end_date_mathches(self, session):
        today = date(3000, 1, 1)
        
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        vacation = VacationFactory(session).create(
            start_date=today,
            end_date=today + timedelta(days=10),
            employee=employee,
        )

        new_start_date = vacation.start_date + timedelta(days=5)
        new_end_date = new_start_date + timedelta(days=10)
        
        result = VacationRepository.merge(
            session,
            employee_id=vacation.employee.id,
            start_date=new_start_date,
            end_date=new_end_date,
            vacation_type=vacation.vacation_type
        )

        assert result == 1
        
        updated_vacation = VacationRepository.get_by_id(session, vacation_id=vacation.id)
        assert updated_vacation.start_date == vacation.start_date
        assert updated_vacation.end_date == new_end_date
    
    def test_does_not_merge_when_different_types(self, session):
        today = date(3000, 1, 1)
        
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        vacation = VacationFactory(session).create(
            start_date=today,
            end_date=today + timedelta(days=10),
            employee=employee,
            vacation_type='paid leave'
        )

        new_start_date = vacation.start_date + timedelta(days=5)
        new_end_date = new_start_date + timedelta(days=10)
        
        result = VacationRepository.merge(
            session,
            employee_id=vacation.employee.id,
            start_date=new_start_date,
            end_date=new_end_date,
            vacation_type="unpaid leave"
        )

        assert result == 0
        
        updated_vacation = VacationRepository.get_by_id(session, vacation_id=vacation.id)
        assert updated_vacation.start_date == vacation.start_date
        assert updated_vacation.end_date == vacation.end_date

    def test_replace_when_all_dates_mathches(self, session):
        today = date(4000, 1, 1)
        
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )
        
        vacation = VacationFactory(session).create(
            start_date=today,
            end_date=today + timedelta(days=10),
            employee=employee,
        )

        new_start_date = vacation.start_date - timedelta(days=10)
        new_end_date = vacation.end_date + timedelta(days=10)
        
        result = VacationRepository.merge(
            session,
            employee_id=vacation.employee.id,
            start_date=new_start_date,
            end_date=new_end_date,
            vacation_type=vacation.vacation_type
        )

        assert result == 2
        
        updated_vacation = VacationRepository.get_by_id(session, vacation_id=vacation.id)
        assert updated_vacation.start_date == new_start_date
        assert updated_vacation.end_date == new_end_date
    
    def test_does_not_merge_if_not_match(self, session):
        today = date(5000, 1, 1)
        
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )
        
        vacation = VacationFactory(session).create(
            start_date=today,
            end_date=today + timedelta(days=10),
            employee=employee,
        )

        new_start_date = vacation.end_date + timedelta(days=10)
        new_end_date = new_start_date + timedelta(days=10)
        
        result = VacationRepository.merge(
            session,
            employee_id=vacation.employee.id,
            start_date=new_start_date,
            end_date=new_end_date,
            vacation_type=vacation.vacation_type
        )

        assert result == 0
    
    def test_get_many_success(self, session):
        employee = EmployeeFactory(session).create(
            first_name='john',
            last_name='doe',
        )

        today = date(5000, 6, 1)
        vacation = VacationFactory(session).create(
            start_date=today,
            end_date=today + timedelta(days=10),
            employee=employee,
        )
        vacation = VacationFactory(session).create(
            start_date=today + timedelta(days=15),
            end_date=today + timedelta(days=20),
            employee=employee,
        )
        vacations = VacationRepository.get_many(session, employee_id=employee.id)
        
        assert len(vacations) > 0
        for vacation in vacations:
            assert vacation.employee_id == employee.id
        
    def test_get_many_returns_empty_list(self, session):
        vacations = VacationRepository.get_many(session, employee_id=uuid.uuid4())
        
        assert vacations == []
