import uuid
import factory
from app.model import EmployeeModel


def EmployeeFactory(session):
    class _EmployeeFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = EmployeeModel
            sqlalchemy_session_persistence = "commit"
            sqlalchemy_session = session

        id = factory.LazyFunction(uuid.uuid4)
        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
    
    return _EmployeeFactory