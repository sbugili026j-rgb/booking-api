from pydantic import BaseModel


class ResourceCreate(BaseModel):
    name: str
    description: str = ""
    capacity: int = 1


class ResourceOut(ResourceCreate):
    id: int
    is_active: bool

    class Config:
        from_attributes = True