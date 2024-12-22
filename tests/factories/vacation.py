from datetime import timedelta
from datetime import date
import uuid
import factory
from app.model import VacationModel
from tests.factories import EmployeeFactory


def VacationFactory(session):
    class _VacationFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = VacationModel
            sqlalchemy_session_persistence = "commit"
            sqlalchemy_session = session

        id = factory.LazyFunction(uuid.uuid4)
        start_date = factory.LazyFunction(lambda: date.today())
        end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=10))
        employee = EmployeeFactory(session).create()
    
    return _VacationFactory