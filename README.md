# Booking API

REST API for reserving rooms, built with Python and FastAPI.

## Features
- User registration and login with JWT tokens
- Passwords hashed with bcrypt, never stored as plain text
- Role-based access: only admins can create rooms
- List bookable rooms (public)
- Book a room for a time slot (login required)
- Double-booking prevention: overlapping times are rejected with a 409 error, while back-to-back bookings are allowed
- Cancel a booking; users can only see and cancel their own
- Input validation with clear error codes (409 conflict, 401 not logged in, 403 not allowed, 404 not found, 422 invalid data)
- 15 automated tests with pytest

## Tech stack
Python, FastAPI, SQLAlchemy, SQLite, pytest

## Run it
```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
Then open `/docs` on the running address for the interactive API page.

## Admin account
Set an environment variable `ADMIN_EMAIL` to your email before starting the app. The account that registers with that email becomes an admin and can create rooms. Set `SECRET_KEY` to a long random value for anything beyond local testing.

## Run tests
```bash
python -m pytest
```

## Endpoints
| Method | Path | Access | What it does |
|---|---|---|---|
| POST | /auth/register | Public | Create an account |
| POST | /auth/login | Public | Log in and get a token |
| GET | /resources | Public | List rooms |
| POST | /resources | Admin | Create a room |
| POST | /bookings | Logged in | Book a room for a time slot |
| GET | /bookings/me | Logged in | List your own bookings |
| DELETE | /bookings/{id} | Logged in | Cancel your booking |

## Ideas for later
- Reject bookings in the past
- Switch from SQLite to PostgreSQL
- Docker setup and a deployed demo