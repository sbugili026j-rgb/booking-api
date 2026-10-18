from datetime import timezone

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, auth
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking API")


def to_naive_utc(dt):
    if dt.tzinfo is not None:
        return dt.astimezone(timezone.utc).replace(tzinfo=None)
    return dt


@app.get("/resources", response_model=list[schemas.ResourceOut])
def list_resources(db: Session = Depends(get_db)):
    return db.query(models.Resource).filter(models.Resource.is_active).all()


@app.post("/resources", response_model=schemas.ResourceOut, status_code=201)
def create_resource(data: schemas.ResourceCreate, db: Session = Depends(get_db)):
    resource = models.Resource(**data.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@app.post("/auth/register", response_model=schemas.UserOut, status_code=201)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = models.User(
        email=data.email,
        hashed_password=auth.hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/auth/login", response_model=schemas.Token)
def login(data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return {"access_token": auth.create_access_token(user.id), "token_type": "bearer"}


@app.post("/bookings", response_model=schemas.BookingOut, status_code=201)
def create_booking(
    data: schemas.BookingCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    start = to_naive_utc(data.start_time)
    end = to_naive_utc(data.end_time)
    if end <= start:
        raise HTTPException(status_code=422, detail="End time must be after start time")

    resource = db.get(models.Resource, data.resource_id)
    if not resource or not resource.is_active:
        raise HTTPException(status_code=404, detail="Resource not found")

    clash = (
        db.query(models.Booking)
        .filter(
            models.Booking.resource_id == data.resource_id,
            models.Booking.status == "confirmed",
            models.Booking.start_time < end,
            models.Booking.end_time > start,
        )
        .first()
    )
    if clash:
        raise HTTPException(
            status_code=409, detail="That time overlaps an existing booking"
        )

    booking = models.Booking(
        user_id=user.id,
        resource_id=data.resource_id,
        start_time=start,
        end_time=end,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@app.get("/bookings/me", response_model=list[schemas.BookingOut])
def my_bookings(
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    return db.query(models.Booking).filter(models.Booking.user_id == user.id).all()


@app.delete("/bookings/{booking_id}", response_model=schemas.BookingOut)
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(auth.get_current_user),
):
    booking = db.get(models.Booking, booking_id)
    if not booking or (booking.user_id != user.id and user.role != "admin"):
        raise HTTPException(status_code=404, detail="Booking not found")
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking
