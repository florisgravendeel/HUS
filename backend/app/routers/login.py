from fastapi import APIRouter

import json
import time
from typing import Optional
from fastapi import Depends, HTTPException, status, Response, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from backend.app.auth import Auth

router = APIRouter()

auth_handler = Auth()
security = HTTPBearer()
SECRET_KEY = "967e64e52668340468d3075c80461de8b22f484487be1fe83c8bd77c2ca06e79"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = 'HS256'

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "johndoe2": {
        "username": "johndoe2",
        "full_name": "Johnny Captian!",
        "email": "johnny@yahoo.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_handler.encode_access_token(user.username)
    token_expiry = auth_handler.get_token_expiry(access_token)

    token_expiry_timestamp = json.dumps(time.mktime(
        token_expiry.timetuple()) * 1000)  # conversion for javascript

    refresh_token = auth_handler.encode_refresh_token(user.username)

    response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=auth_handler.COOKIE_MAX_AGE)
    return {"access_token": access_token, "token_type": "bearer", "token_expiry": token_expiry_timestamp}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")  # it only resets cookies, so no access is required to logout
    response.status_code = status.HTTP_200_OK  # what if someone else forces another to logout? mmh paranoia
    return response


@router.post("/refresh_token")
async def refresh_token_(request: Request, response: Response):
    refresh_token = request.cookies.get('refresh_token')  # What to do with 401?
    user_id = auth_handler.decode_refresh_token(refresh_token)

    new_access_token = auth_handler.encode_access_token(user_id)
    token_expiry = auth_handler.get_token_expiry(new_access_token)

    token_expiry_timestamp = json.dumps(time.mktime(
        token_expiry.timetuple()) * 1000)  # conversion for javascript

    new_refresh_token = auth_handler.encode_refresh_token(user_id)
    response.set_cookie("refresh_token", new_refresh_token, httponly=True, max_age=auth_handler.COOKIE_MAX_AGE)
    return {"access_token": new_access_token, "token_type": "bearer", "token_expiry": token_expiry_timestamp}


@router.post("/users/me/")
def my_profile(credentials: HTTPAuthorizationCredentials = Security(security)):
    access_token = credentials.credentials
    username = auth_handler.decode_access_token(access_token)
    if username:
        return 'Welcome ' + username
