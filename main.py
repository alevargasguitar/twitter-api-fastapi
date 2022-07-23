# Python
from datetime import date
from uuid import UUID
from typing import Optional

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# fastAPI
from fastapi import FastAPI


app = FastAPI()

# Models

class UserBase(BaseModel):
    user_ID: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
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
    birth_date: Optional[date] = Field(default=None)

class Tweet():
    pass


@app.get(path="/")
def home():
    return {"Twitter API": "Working!"}