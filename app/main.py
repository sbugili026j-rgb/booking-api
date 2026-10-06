from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Booking API")


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