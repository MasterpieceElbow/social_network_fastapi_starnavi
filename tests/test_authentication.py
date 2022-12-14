import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.dependencies import get_db
from db.database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_sign_up(test_db):
    response = client.post(
        "/api/sign-up/",
        data={"username": "user1", "password": "password1"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "username": "user1",
        "posts": [],
        "last_login": None,
        "last_request": None,
    }


def test_login(test_db):
    client.post(
        "/api/sign-up/",
        data={"username": "user1", "password": "password1"}
    )
    response = client.post(
        "/api/token/",
        data={"username": "user1", "password": "password1"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("access_token") is not None
    assert response.json().get("token_type") == "bearer"
