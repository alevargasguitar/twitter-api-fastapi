# Python
from datetime import datetime
from doctest import Example
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel, PaymentCardNumber
from pydantic import EmailStr
from pydantic import Field
# from email_validator import validate_email, EmailNotValidError

# FastAPI
from fastapi import FastAPI, Path
from fastapi import Body, Query, Path

app = FastAPI()

# Models

# class Email(email):
#     email = EmailStr

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50
        )

    class Config:
        schema_extra = {
            "example": {
                "city": "CDMX",
                "state": "CDMX",
                "country": "México"
            }
        }


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Alejandro"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Vargas"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example="25"
    )
    hair_color: Optional[HairColor] = Field(default=None, example="red")
    is_married: Optional[bool] = Field(default=None, example=False)
    email: Optional[EmailStr] = Field(default=None, example="ale@vargas.com")
    date: Optional[datetime] = Field(default=None, example="2022-07-22T01:59:55")

class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example="HolaSoyMiguel"
        )
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "García Martoni",
    #             "age": 20,
    #             "hair_color": "blonde",
    #             "is_married": False,
    #             "email": "facundo@email.com",
    #             "date": "2022-07-22 01:59:55",
    #             #"card": "123423453456#5467"
    #         }
    #     }

class PersonOut(PersonBase):
    pass

@app.get("/")
def home():
    return {"Hello": "World"}

#Request and Response body

@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_lenght=1,
        max_length=50,
        title="Person Name",
        description="This is te person name. Its betwen 1 and 50 characters",
        example="Rocío"
        ),
    age: int = Query(
        ...,
        title="Persona Age",
        description="This is the person age. Its required",
        example=25
    )
):
    return {name: age}

# Validaciones: Path Parameters
@app.get("/person/detail{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=135
        )
):
    return {person_id: "It exist!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=135
    ),
    person: Person = Body(...),
    Location: Location = Body(...)
):
    results = person.dict()
    results.update(Location.dict())
    return results