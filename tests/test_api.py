ROOM = {"name": "Meeting Room A", "description": "Projector", "capacity": 8}


def test_register_and_login(client):
    body = {"email": "tester1@gmail.com", "password": "strongpass123"}
    response = client.post("/auth/register", json=body)
    assert response.status_code == 201
    assert response.json()["email"] == "tester1@gmail.com"
    assert "password" not in response.json()

    response = client.post("/auth/login", json=body)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_duplicate_email_is_rejected(client):
    body = {"email": "tester2@gmail.com", "password": "strongpass123"}
    assert client.post("/auth/register", json=body).status_code == 201
    assert client.post("/auth/register", json=body).status_code == 409


def test_wrong_password_is_rejected(client):
    body = {"email": "tester3@gmail.com", "password": "strongpass123"}
    client.post("/auth/register", json=body)
    bad = {"email": "tester3@gmail.com", "password": "wrongpass999"}
    assert client.post("/auth/login", json=bad).status_code == 401


def test_short_password_is_rejected(client):
    body = {"email": "tester4@gmail.com", "password": "short"}
    assert client.post("/auth/register", json=body).status_code == 422


def test_admin_can_create_and_list_resource(client, admin_headers):
    response = client.post("/resources", json=ROOM, headers=admin_headers)
    assert response.status_code == 201
    names = [r["name"] for r in client.get("/resources").json()]
    assert "Meeting Room A" in names


def test_resource_creation_requires_login(client):
    response = client.post("/resources", json=ROOM)
    assert response.status_code in (401, 403)


def test_normal_user_cannot_create_resource(client):
    body = {"email": "regular@gmail.com", "password": "strongpass123"}
    client.post("/auth/register", json=body)
    token = client.post("/auth/login", json=body).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/resources", json=ROOM, headers=headers)
    assert response.status_code == 403
