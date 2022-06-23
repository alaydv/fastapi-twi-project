# Python
import json
from uuid import UUID,uuid4
from datetime import date, datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel, Field
from pydantic import EmailStr, SecretStr

# FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body


app = FastAPI()

# Models
class BaseUser(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
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
    birth_date: Optional[date] = Field(default=None)

class UserRegister(User):
    password: SecretStr = Field(
        ...,
        min_length=8
    )

class Tweet(BaseModel):
    tweet_id: UUID = Field(default_factory=uuid4)
    content: str = Field(
        ...,
        min_length=1,
        max_length=280
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
    summary="Create a user",
    tags=["Users"]
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters:
    - Request Body Parameter:
        - **user: UserRegister**

    Returns a user model:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_day: date
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        user_dict["password"] = str(user_dict["password"])
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

    This path operation show all user in the app

    Parameters:
        -

    Returns all users whit the following info:
    - user_id: UUID
    - email: EmailStr
    - first_name: str
    - last_name: str
    - birth_day: date
    """
    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Show a user
@app.get(
    path="/user/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a user",
    tags=["Users"]
)
def show_a_user():
    pass

### Update a user
@app.put(
    path="/user/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a user",
    tags=["Users"]
)
def update_user():
    pass

### Delete a user
@app.delete(
    path="/user/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
def delete_user():
    pass

## Tweets

### Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all Tweets",
    tags=["Tweets"]
    )
def home():
    """
    Show all tweets

    This path operation show all tweets in the app

    Parameters:
        -

    Return a json with all tweets in the app whit the following info:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)):
    """
    Post a tweet

    This path operation creates a new tweet in the app

    Parameters:
    - Request Body:
        - **tweet: Tweet**

    Return a tweet whit the following info:
    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        results = json.loads(f.read())
        tweets_dict = tweet.dict()
        tweets_dict["tweet_id"] = str(tweets_dict["tweet_id"])
        tweets_dict["created_at"] = str(tweets_dict["created_at"])
        tweets_dict["updated_at"] = str(tweets_dict["updated_at"])
        tweets_dict["by"]["user_id"] = str(tweets_dict["by"]["user_id"])
        tweets_dict["by"]["birth_date"] = str(tweets_dict["by"]["birth_date"])
        results.append(tweets_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a Tweet",
    tags=["Tweets"]
)
def show_a_tweet():
    pass

### Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a Tweet",
    tags=["Tweets"]
)
def update_a_tweet():
    pass

### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a Tweet",
    tags=["Tweets"]
)
def delete_a_tweet():
    pass
