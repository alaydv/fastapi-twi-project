# Python
from uuid import UUID
from datetime import date
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr, SecretStr

# FastApi
from fastapi import FastAPI

app = FastAPI()

# Models
class BaseUser(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)


class UserLogin(BaseUser):
    password: SecretStr = Field(
        ...,
        min_length=8
    )

class User(BaseUser):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_day: Optional[date] = Field(default=None)

class Teewt(BaseModel):
    pass

@app.get(path="/")
def home():
    return {"Twiter API": "Working"}