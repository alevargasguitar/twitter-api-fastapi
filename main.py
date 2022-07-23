# Python
from datetime import datetime
from typing import Optional
from enum import Enum
import fastapi

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
# from email_validator import validate_email, EmailNotValidError

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Path, Cookie, UploadFile, File

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

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")


@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home of the app"
    )
def home():
    """
    Home
    
    This path operation show a Hello World

    Parameters:
    - It doesn't have any parameter
    
    Return a string: "Hello World"
    """
    return {"Hello": "World"}

#Request and Response body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the app"
    )
def create_person(person: Person = Body(...)):
    """
    Create Person
    
    This path operation create a person in the app and save the information in the database

    Parameters:
    - Request Body Parameter:
        - **person: Person** -> A person Model with first name, last name, hair color, age and marital state
    
    Return a person model with first name, last name, age, hair color and marital state
    """
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary=["Shows Person's detail"],
    deprecated=True
    )
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
        title="Person Age",
        description="This is the person age. Its required",
        example=25
    )
):
    """
    Show Person
    
    This path operation show name and age of the person in the app

    Parameters:
    - Request Query Parameter:
        - **name: Optional[str]** -> This is te person name. Its betwen 1 and 50 characters
        - **age: int** -> This is the person age. Its required
    
    Return a person model with first name, last name, age, hair color and marital state
    """
    return {name: age}

# Validaciones: Path Parameters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary=["GET Person's ID"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=135
        )
):
    """
    Show Person
    
    This path parameter GET the person's ID

    Parameters:
    - Request Path Parameter:
        - **person_id: int** -> It's the person's ID, should be great than 0.
    
    Return a person's ID
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist!"
        )
    return {person_id: "It exist!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary={"UPDATE Person´s ID"}
    )
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
    """
    Show Person
    
    This path parameter UPDATE the person's ID

    Parameters:
    - Request Path Parameter:
        - **person_id: int** -> It's the person's ID, should be great than 0.
    
    Return a person's ID and Location
    """
    results = person.dict()
    results.update(Location.dict())
    return results

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
)
def login(userame: str = Form(...), password: str = Form(...)):
    return LoginOut(username=userame)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Cookies and Headers"]
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1,
    ),
    emainl: EmailStr = Form(
        ...,
    ),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# Files

@app.post(
    path="/post-image",
    tags=["Files"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filaname": image.filename,
        "Format": image.content_type,
        "Size(Kb)": round((len(image.file.read()))/1024, ndigits=2)
    }
