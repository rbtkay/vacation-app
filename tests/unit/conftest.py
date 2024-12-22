import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.model.base import BaseModel

TEST_DATABASE_URL = "sqlite:///:memory:"

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