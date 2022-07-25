# Python
import json
from unittest import result
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel, EmailStr, Field

# fastAPI
from fastapi import Body, FastAPI
from fastapi import status


app = FastAPI()

# Models

class UserBase(BaseModel):
    user_ID: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
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

class UserRegister(User):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )

class Tweet(BaseModel):
    tweet_ID: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)


# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User, 
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
    )

def signup(user: UserRegister = Body(...)):
    """
    Signup
    
    This Path Operation register a user in the app

    Parameters:
        - Request Body Parameter
            - user: UserRegister

    Returns a json with the basic user information:
        - user_ID: UUID
        - email: EmailStr
        - fist_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_ID"] = str(user_dict["user_ID"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user

### Login a user
@app.post(
    path="/login",
    response_model=User, 
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
    )

def login():
    pass

### Show all users
@app.get(
    path="/users",
    response_model=List[User], 
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
    )

def show_all_users():
    """
    Show all users

    This path operations shows all users in the app

    Parameters:
        -
    
    Returns a json list with all users in the app, with the following keys
        - user_ID: UUID
        - email: EmailStr
        - fist_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/users/{user_ID}",
    response_model=User, 
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
    )

def show_a_user():
    pass

### Delete a user
@app.delete(
    path="/users/{user_ID}/delete",
    response_model=User, 
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
    )

def delete_a_user():
    pass

### Update a user
@app.put(
    path="/users/{user_ID}/update",
    response_model=User, 
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
    )

def update_a_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet], 
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    return {"Twitter API": "Working!"}

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet, 
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)

def post(tweet: Tweet = Body(...)):
    """
    Post a tweets
    
    This Path Operation post a tweet in the app

    Parameters:
        - Request Body Parameter
            - user: Tweet

    Returns a json with the basic tweet information:
        - tweet_ID: UUID
        - content: str
        - created_at: datetime
        - updated_at: datetime
        - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_ID"] = str(tweet_dict["tweet_ID"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_ID"] = str(tweet_dict["by"]["user_ID"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweets_ID}",
    response_model=Tweet, 
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)

def show_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweets_ID}/delete",
    response_model=Tweet, 
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)

def delete_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweets_ID}/update",
    response_model=Tweet, 
    status_code=status.HTTP_200_OK,
    summary="Udate a tweet",
    tags=["Tweets"]
)

def update_a_tweet():
    pass