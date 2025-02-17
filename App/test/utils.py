from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from fastapi.testclient import TestClient
from ..models import Todos, Users
import pytest
from ..main import app
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'ulrichjato', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()  # Open test database session
    db.add(todo)  # Add test data (a new todo item)
    db.commit()  # Save the new todo in the test database

    yield db  # Pause here and allow the test to run

    # Clean up the test database after the test finishes
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username = "ulrichjato",
        email = "urichjato@email.com",
        first_name = "Ulrich",
        last_name = "Guiffo",
        hashed_password = bcrypt_context.hash("testpassword"),
        role = "admin",
        phone_number = "(111)-111-1111"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield db
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()