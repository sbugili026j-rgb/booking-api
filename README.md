# Booking API

REST API for reserving rooms, built with Python and FastAPI.

## Features
- User registration and login with JWT tokens
- Passwords hashed with bcrypt, never stored as plain text
- Create and list bookable rooms
- Input validation with clear error codes (409 duplicate email, 401 wrong login, 422 invalid data)
- Automated tests with pytest

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
| Method | Path | What it does |
|---|---|---|
| POST | /auth/register | Create an account |
| POST | /auth/login | Log in and get a token |
| GET | /resources | List rooms |
| POST | /resources | Create a room |

## Coming next
- Bookings with double-booking prevention
- Admin-only room creation