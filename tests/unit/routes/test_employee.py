import uuid
from tests.factories import EmployeeFactory
from tests.factories import VacationFactory
from app.repository.employee import EmployeeRepository

from datetime import date
from datetime import timedelta

class TestEmployeeGetEndpoints:
    def test_get_nominal(self, client, session):
        employee = EmployeeFactory(session).create()

        response = client.get(f"/employee/{employee.id}")
        assert response.status_code == 200

    def test_get_404(self, client):
        response = client.get(f"/employee/{uuid.uuid4()}")
        assert response.status_code == 404

class TestEmployeePostEndpoints:
    def test_post_nominal(self, client):
        payload = {
            "first_name": 'John',
            "last_name": 'Doe',
        }
        response = client.post(f"/employee", json=payload)
    
        assert response.status_code == 201

        response_data = response.json()
        assert response_data["first_name"] == "John"
        assert response_data["last_name"] == "Doe"
        assert "id" in response_data

class TestEmployeeGetAllEndpoints:
    def test_get_all(self, client, session):
        EmployeeFactory(session).create(),
        EmployeeFactory(session).create(),
        EmployeeFactory(session).create()
    
        response = client.get(f"/employee")
        assert response.status_code == 200

        response_data = response.json()

        for employee in response_data:
            assert employee['id'] is not None
            assert employee['first_name'] is not None
            assert employee['last_name'] is not None

class TestEmployeeGetVacationsEndpoints:
    def test_get_employee_vacations(self, client, session):
        employee = EmployeeFactory(session).create()

        vacations = [
            VacationFactory(session).create(employee=employee),
            VacationFactory(session).create(employee=employee),
            VacationFactory(session).create(employee=employee)
        ]

        response = client.get(f"/employee/{employee.id}/vacations")
        assert response.status_code == 200

        response_data = response.json()
        len(response_data) == 3

        assert response_data[0]['id'] == str(vacations[0].id)
        assert response_data[1]['id'] == str(vacations[1].id)
        assert response_data[2]['id'] == str(vacations[2].id)
    
    def test_get_employee_vacations_returns_empty_list(self, client, session):
        employee = EmployeeFactory(session).create()

        response = client.get(f"/employee/{employee.id}/vacations")
        assert response.status_code == 200

        response_data = response.json()
        assert response_data == []
    
    def test_get_employee_vacations_raises_404_when_no_employee(self, client, session):
        response = client.get(f"/employee/{uuid.uuid4()}/vacations")
        assert response.status_code == 404


class TestEmployeeGetOffsEndpoints:
    def test_get_employee_in_vacation_nominal(self, client, session):
        employee = EmployeeFactory(session).create()

        start_date = date(2000, 1, 1)
        end_date = start_date + timedelta(days=10)
        VacationFactory(session).create(
            start_date=start_date,
            end_date=end_date,
            employee=employee,
        )
        
        requested_date = date(2000, 1, 5)
        response = client.get(f"/employee/off/{requested_date}")

        assert response.status_code == 200
    
    def test_get_employee_in_vacation_raises_422_when_no_date(self, client, session):
        response = client.get(f"/employee/off")
        assert response.status_code == 422
