import uuid
from datetime import date
from datetime import timedelta

from app.repository.employee import EmployeeRepository
from app.repository.vacation import VacationRepository

from tests.factories import EmployeeFactory
from tests.factories import VacationFactory

class TestEmployeeRepository:
    def setup_method(self):
        self.id = uuid.uuid4()
        self.first_name = 'robert'
        self.last_name = 'khayat'

    def test_create_employee(self, session):
        new_employee = EmployeeFactory(session).create()

        employee = EmployeeRepository.get_by_id(session, new_employee.id)
        
        assert employee.id == new_employee.id
        assert employee.first_name == new_employee.first_name
        assert employee.last_name == new_employee.last_name
    
    def test_get_employee_in_vacation_nominal(self, session):
        employee_1 = EmployeeFactory(session).create(
            first_name="john",
            last_name="doe",
        )
        employee_2 = EmployeeFactory(session).create(
            first_name="jane",
            last_name="doe",
        )
        
        start_date_1 = date(2000, 1, 1)
        end_date_1 = start_date_1 + timedelta(days=10)
        VacationFactory(session).create(
            start_date=start_date_1,
            end_date=end_date_1,
            employee=employee_1,

        )
        
        start_date_2 = date(2000, 1, 5)
        end_date_2 = start_date_2 + timedelta(days=10)
        VacationFactory(session).create(
            start_date=start_date_2,
            end_date=end_date_2,
            employee=employee_2
        )

        start_date_3 = date(2000, 5, 1)
        end_date_3 = start_date_3 + timedelta(days=10)
        VacationFactory(session).create(
            start_date=start_date_3,
            end_date=end_date_3,
            employee=employee_1
        )
        
        start_date_4 = date(2000, 3, 1)
        end_date_4 = start_date_4 + timedelta(days=10)
        VacationFactory(session).create(
            start_date=start_date_4,
            end_date=end_date_4,
            employee=employee_2
        )
        
        date_requested = date(2000, 1, 8)
        employees_in_vacation = EmployeeRepository.get_in_vacation(
            session,
            first_name='john',
            requested_date=date_requested,
        )

        assert len(employees_in_vacation) == 1
        assert employees_in_vacation[0].id == employee_1.id

        employees_in_vacation = EmployeeRepository.get_in_vacation(
            session,
            first_name='jane',
            requested_date=date_requested,
        )

        assert len(employees_in_vacation) == 1

        employees_in_vacation = EmployeeRepository.get_in_vacation(
            session,
            requested_date=date_requested
        )
        assert len(employees_in_vacation) == 2
        assert employees_in_vacation[0].id == employee_1.id