from fastapi import APIRouter

import json
import time
from typing import Optional
from fastapi import Depends, HTTPException, status, Response, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.app.libary.auth_token import AuthToken
from backend.app.libary.auth_user import AuthUser

router = APIRouter()

token_handler = AuthToken()
user_auth = AuthUser()
security = HTTPBearer()

SECRET_KEY = "967e64e52668340468d3075c80461de8b22f484487be1fe83c8bd77c2ca06e79"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = 'HS256'


@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    After an valid authentication, the server will respond with a refresh token in form
    of a httponly-cookie and an access token. Both are JSON Web Tokens (JWT).
    """
    user = user_auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = token_handler.encode_access_token(user.username)
    token_expiry = token_handler.get_token_expiry(access_token)

    token_expiry_timestamp = json.dumps(time.mktime(
        token_expiry.timetuple()) * 1000)  # conversion for javascript

    refresh_token = token_handler.encode_refresh_token(user.username)

    response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=token_handler.COOKIE_MAX_AGE)
    return {"access_token": access_token, "token_type": "bearer", "token_expiry": token_expiry_timestamp}


@router.post("/logout")
async def logout(response: Response):
    """
    For an user to fully logout, we need the backend to send us a response
    to delete the httponly cookie, since we cannot delete the cookie in the frontend.
    """
    response.delete_cookie("refresh_token")  # it only resets cookies, so no access is required to logout
    response.status_code = status.HTTP_200_OK
    return response


@router.post("/refresh_token")
async def refresh_token_(request: Request, response: Response):
    """
    Our access token expires after a while, a valid refresh token is required to get an new access token.
    Returns a new refresh token and an new access token.
    """
    refresh_token = request.cookies.get('refresh_token')
    user_id = token_handler.decode_refresh_token(refresh_token)

    new_access_token = token_handler.encode_access_token(user_id)
    token_expiry = token_handler.get_token_expiry(new_access_token)

    token_expiry_timestamp = json.dumps(time.mktime(
        token_expiry.timetuple()) * 1000)  # conversion for javascript

    new_refresh_token = token_handler.encode_refresh_token(user_id)
    response.set_cookie("refresh_token", new_refresh_token, httponly=True, max_age=token_handler.COOKIE_MAX_AGE)
    return {"access_token": new_access_token, "token_type": "bearer", "token_expiry": token_expiry_timestamp}


@router.post("/users/me/")
def my_profile(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    After the user logged in, we want to retrieve their profile from our database and return it to them.
    """
    access_token = credentials.credentials
    username = token_handler.decode_access_token(access_token)
    if username:
        return 'Welcome ' + username
