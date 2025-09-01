from ast import pattern
from pydantic import BaseModel, Field
import datetime

class UserCreateRequest(BaseModel):
    username: str
    email: str = Field(is_email=True)
    password: str = Field(min_length=8, max_length=16)
    phone_number: str = Field(min_length=10, max_length=10)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str = Field(is_email=True)
    phone_number: str = Field(min_length=10, max_length=10, pattern=r"^[0-9]+$")
    balance: float = Field(ge=0)
    created_at: datetime.datetime

class UserUpdateRequest(BaseModel):
    username: str
    phone_number: str = Field(min_length=10, max_length=10, pattern=r"^[0-9]+$")