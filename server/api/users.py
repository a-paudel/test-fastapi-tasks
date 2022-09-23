from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from prisma.models import User, Token
from passlib.hash import argon2
from server.auth import get_token, get_user
from server.database import db
from pydantic import BaseModel

user_router = APIRouter(prefix="/users", tags=["User"])


# SCHEMAS
class UserOutput(BaseModel):
    # id username
    id: str
    username: str


class TokenOutput(BaseModel):
    # access_token expiry_date token_type user_id
    access_token: str
    expiry_date: datetime
    token_type: str
    user_id: str


# login
@user_router.post(
    "/login",
    response_model=TokenOutput,
    status_code=201,
    responses={401: {}},
)
async def login(data: OAuth2PasswordRequestForm = Depends()):
    user = await db.user.find_unique(where={"username": data.username})
    if user and argon2.verify(data.password, user.password):
        token = await db.token.create(data={"user_id": user.id})
        return token
    raise HTTPException(status_code=401, detail="Invalid username or password")


# register
@user_router.post(
    "/register",
    response_model=TokenOutput,
    status_code=201,
    responses={400: {}},
)
async def register(data: OAuth2PasswordRequestForm = Depends()):
    user = await db.user.find_unique(where={"username": data.username})
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = argon2.hash(data.password)
    user = await db.user.create(
        data={"username": data.username, "password": hashed_password}
    )
    token = await db.token.create(data={"user_id": user.id})
    return token


# me
@user_router.get(
    "/me",
    response_model=UserOutput,
    # responses={401: {}},
)
async def me(user: User = Depends(get_user)):
    return user


# logout
@user_router.delete(
    "/logout",
    status_code=204,
    responses={401: {}},
)
async def logout(token: Token = Depends(get_token)):
    await db.token.delete(where={"id": token.id})


# logout all
@user_router.delete(
    "/logout/all",
    status_code=204,
    responses={401: {}},
)
async def logout_all(user: User = Depends(get_user)):
    await db.token.delete_many(where={"user_id": user.id})
