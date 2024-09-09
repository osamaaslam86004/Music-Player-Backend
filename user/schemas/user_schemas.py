from pydantic.fields import Field
from pydantic import BaseModel


# Pydantic models for user input
class UserCreate(BaseModel):
    username: str = Field(..., min_length=10, max_length=25, description="Name of User")
    password: str = Field(..., min_length=10, max_length=25, description="Password")

    class Config:
        json_schema_extra = {
            "example": {"username": "abdulazeezx_com", "password": "weakpassword"}
        }


class UserLogin(UserCreate):
    pass
