import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import io

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def make_image():
    return ("test.png", io.BytesIO(b"fake image content"), "image/png")

def test_register_user():
    response = client.post("/users/register", json={
        "username": "testuser",
        "password": "1234"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_register_duplicate_user():
    client.post("/users/register", json={"username": "testuser", "password": "1234"})
    response = client.post("/users/register", json={"username": "testuser", "password": "1234"})
    assert response.status_code == 409

def test_login_user():
    client.post("/users/register", json={"username": "testuser", "password": "1234"})
    response = client.post("/users/login", data={"username": "testuser", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/users/register", json={"username": "testuser", "password": "1234"})
    response = client.post("/users/login", data={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401

def test_create_post_authenticated():
    client.post("/users/register", json={"username": "testuser", "password": "1234"})
    login = client.post("/users/login", data={"username": "testuser", "password": "1234"})
    token = login.json()["access_token"]
    response = client.post("/posts/",
        data={"title": "Test Post", "description": "Test Description"},
        files={"image": make_image()},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Post"

def test_create_post_unauthenticated():
    response = client.post("/posts/",
        data={"title": "Test Post"},
        files={"image": make_image()}
    )
    assert response.status_code == 401

def test_get_posts_public():
    response = client.get("/posts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_post_wrong_user():
    client.post("/users/register", json={"username": "user1", "password": "1234"})
    client.post("/users/register", json={"username": "user2", "password": "1234"})
    login1 = client.post("/users/login", data={"username": "user1", "password": "1234"})
    login2 = client.post("/users/login", data={"username": "user2", "password": "1234"})
    token1 = login1.json()["access_token"]
    token2 = login2.json()["access_token"]
    post = client.post("/posts/",
        data={"title": "User1 Post"},
        files={"image": make_image()},
        headers={"Authorization": f"Bearer {token1}"}
    )
    post_id = post.json()["id"]
    response = client.delete(f"/posts/{post_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )
    assert response.status_code == 403