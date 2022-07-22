# Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Path
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

#Request and Response body

@app.post("/person/new")
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
        ),
    age: int = Query(
        ...,
        title="Persona Age",
        description="This is the person age. Its required"
    )
):
    return {name: age}

# Validaciones: Path Parameters
@app.get("/person/detail{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0
        )
):
    return {person_id: "It exist!"}