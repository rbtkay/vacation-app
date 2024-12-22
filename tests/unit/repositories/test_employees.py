from app.repository.employee import EmployeeRepository


class TestEmployeeRepository:
    def setup_method(self):
        self.first_name = 'robert'
        self.last_name = 'khayat'

    def test_create_employee(self, session):
        new_employee = EmployeeRepository.create(
            session,
            first_name=self.first_name,
            last_name=self.last_name,
        )

        employee = EmployeeRepository.get_by_id(session, new_employee.id)
        
        assert employee.id == new_employee.id
        assert employee.first_name == new_employee.first_name
        assert employee.last_name == new_employee.last_name