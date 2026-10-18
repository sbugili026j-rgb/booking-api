from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ResourceCreate(BaseModel):
    name: str
    description: str = ""
    capacity: int = 1


class ResourceOut(ResourceCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
