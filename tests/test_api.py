from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSession = sessionmaker(bind=engine, autoflush=False)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_register_and_login():
    body = {"email": "tester1@gmail.com", "password": "strongpass123"}
    response = client.post("/auth/register", json=body)
    assert response.status_code == 201
    assert response.json()["email"] == "tester1@gmail.com"
    assert "password" not in response.json()

    response = client.post("/auth/login", json=body)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_duplicate_email_is_rejected():
    body = {"email": "tester2@gmail.com", "password": "strongpass123"}
    assert client.post("/auth/register", json=body).status_code == 201
    assert client.post("/auth/register", json=body).status_code == 409


def test_wrong_password_is_rejected():
    body = {"email": "tester3@gmail.com", "password": "strongpass123"}
    client.post("/auth/register", json=body)
    bad = {"email": "tester3@gmail.com", "password": "wrongpass999"}
    assert client.post("/auth/login", json=bad).status_code == 401


def test_short_password_is_rejected():
    body = {"email": "tester4@gmail.com", "password": "short"}
    assert client.post("/auth/register", json=body).status_code == 422


def test_create_and_list_resource():
    room = {"name": "Meeting Room A", "description": "Projector", "capacity": 8}
    assert client.post("/resources", json=room).status_code == 201
    names = [r["name"] for r in client.get("/resources").json()]
    assert "Meeting Room A" in names
