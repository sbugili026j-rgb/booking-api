from sqlalchemy import Column, Integer, String, Boolean
from .database import Base


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, default="")
    capacity = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)