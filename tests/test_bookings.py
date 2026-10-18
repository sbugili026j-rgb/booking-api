def auth_headers(client, email="user1@gmail.com"):
    body = {"email": email, "password": "strongpass123"}
    client.post("/auth/register", json=body)
    token = client.post("/auth/login", json=body).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def make_room(client, admin_headers):
    room = {"name": "Room A", "description": "", "capacity": 4}
    return client.post("/resources", json=room, headers=admin_headers).json()["id"]


def slot(room_id, start_hour, end_hour):
    return {
        "resource_id": room_id,
        "start_time": f"2030-01-01T{start_hour}:00:00",
        "end_time": f"2030-01-01T{end_hour}:00:00",
    }


def test_booking_requires_login(client, admin_headers):
    room_id = make_room(client, admin_headers)
    response = client.post("/bookings", json=slot(room_id, "10", "12"))
    assert response.status_code in (401, 403)


def test_create_booking(client, admin_headers):
    headers = auth_headers(client)
    room_id = make_room(client, admin_headers)
    response = client.post("/bookings", json=slot(room_id, "10", "12"), headers=headers)
    assert response.status_code == 201
    assert response.json()["status"] == "confirmed"


def test_overlapping_booking_is_rejected(client, admin_headers):
    headers = auth_headers(client)
    room_id = make_room(client, admin_headers)
    assert client.post("/bookings", json=slot(room_id, "10", "12"), headers=headers).status_code == 201
    response = client.post("/bookings", json=slot(room_id, "11", "13"), headers=headers)
    assert response.status_code == 409


def test_back_to_back_bookings_are_allowed(client, admin_headers):
    headers = auth_headers(client)
    room_id = make_room(client, admin_headers)
    assert client.post("/bookings", json=slot(room_id, "10", "12"), headers=headers).status_code == 201
    assert client.post("/bookings", json=slot(room_id, "12", "14"), headers=headers).status_code == 201


def test_end_before_start_is_rejected(client, admin_headers):
    headers = auth_headers(client)
    room_id = make_room(client, admin_headers)
    response = client.post("/bookings", json=slot(room_id, "12", "10"), headers=headers)
    assert response.status_code == 422


def test_cancelling_frees_the_slot(client, admin_headers):
    headers = auth_headers(client)
    room_id = make_room(client, admin_headers)
    booking = client.post("/bookings", json=slot(room_id, "10", "12"), headers=headers).json()
    cancelled = client.delete(f"/bookings/{booking['id']}", headers=headers)
    assert cancelled.status_code == 200
    assert cancelled.json()["status"] == "cancelled"
    assert client.post("/bookings", json=slot(room_id, "10", "12"), headers=headers).status_code == 201


def test_cannot_cancel_someone_elses_booking(client, admin_headers):
    owner = auth_headers(client, "owner@gmail.com")
    other = auth_headers(client, "other@gmail.com")
    room_id = make_room(client, admin_headers)
    booking = client.post("/bookings", json=slot(room_id, "10", "12"), headers=owner).json()
    response = client.delete(f"/bookings/{booking['id']}", headers=other)
    assert response.status_code == 404


def test_my_bookings_only_shows_own(client, admin_headers):
    owner = auth_headers(client, "owner@gmail.com")
    other = auth_headers(client, "other@gmail.com")
    room_id = make_room(client, admin_headers)
    client.post("/bookings", json=slot(room_id, "10", "12"), headers=owner)
    assert len(client.get("/bookings/me", headers=owner).json()) == 1
    assert client.get("/bookings/me", headers=other).json() == []
