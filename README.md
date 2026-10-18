# Booking API

REST API for reserving rooms, built with Python and FastAPI.

## Features
- User registration and login with JWT tokens
- Passwords hashed with bcrypt, never stored as plain text
- Create and list bookable rooms
- Book a room for a time slot (login required)
- Double-booking prevention: overlapping times are rejected with a 409 error, while back-to-back bookings are allowed
- Cancel a booking; users can only see and cancel their own
- Input validation with clear error codes (409 conflict, 401 wrong login, 404 not found, 422 invalid data)
- 13 automated tests with pytest

## Tech stack
Python, FastAPI, SQLAlchemy, SQLite, pytest

## Run it
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Then open `/docs` on the running address for the interactive API page.

## Run tests
```bash
python -m pytest
```

## Endpoints
| Method | Path | Login needed | What it does |
|---|---|---|---|
| POST | /auth/register | No | Create an account |
| POST | /auth/login | No | Log in and get a token |
| GET | /resources | No | List rooms |
| POST | /resources | No | Create a room |
| POST | /bookings | Yes | Book a room for a time slot |
| GET | /bookings/me | Yes | List your own bookings |
| DELETE | /bookings/{id} | Yes | Cancel your booking |

## Coming next
- Admin-only room creation