from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.base import BaseModel
from app.main import app
from app.db.session import get_db

TEST_DATABASE_URL = "sqlite:///test.db" #"sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_test_database():
    """Set up the test database by creating all tables."""
    BaseModel.metadata.create_all(bind=engine)

def teardown_test_database():
    """Tear down the test database by dropping all tables."""
    BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    """Set up and tear down the test database."""
    setup_test_database()  # Create tables before tests
    yield  # Run tests
    teardown_test_database()  # Drop tables after tests


@pytest.fixture
def session():
    """Fixture to provide a test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    app.dependency_overrides[get_db] = lambda: session  # Use SQLite for tests

    with TestClient(app) as c:
        yield c

    app.dependency_overrides = {}  # Reset overrides after tests


# @pytest.fixture
# def mock_sessionmaker(session):
#     mock_fastapi_sessionmaker = mock.MagicMock()
#     def mock_get_db():
#         yield session
    
#     # mock_fastapi_sessionmaker.get_db.side_effect = mock_get_db

#     with mock.patch('app.db.session._get_fastapi_sessionmaker', return_value=mock_fastapi_sessionmaker):
#         yield

# @pytest.fixture
# def mock_session_api(session):
#     with mock.patch('app.api.routes.employee.get_db', mock.MagicMock()):
#         yield

# @pytest.fixture
# def client():
#     """Fixture to provide a TestClient for the FastAPI app."""
#     client = TestClient(app)
#     yield client  
