from typing import Optional
from fastapi import Depends, HTTPException, status, Response, Request, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


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


class AuthUser:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = "967e64e52668340468d3075c80461de8b22f484487be1fe83c8bd77c2ca06e79"
        self.ALGORITHM = 'HS256'
        self.fake_users_db = {
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

    def authenticate(self, username: str, password: str):
        """
        Authenticates the user and password.
        :return False when username or password is wrong.
        :return True when username and password is correct.
        """
        user = self.get_user(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return True

    def get_user(self, username: str):
        """
        Returns the user, based of the username.
        :return User object
        """
        if username in self.fake_users_db:
            user_dict = self.fake_users_db[username]
            return UserInDB(**user_dict)

    def get_profile(self, username: str):
        """
        Returns the user, based of the username.
        :return User object in dictionary
        """
        if username in self.fake_users_db:
            user_dict = self.fake_users_db[username]
            return user_dict

    def verify_password(self, plain_password, hashed_password):
        """
        Verifies the plain password with the hashed password.
        :return True when password and the hash matches
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        """
        Hashes the text password into a hash password
        :param password: plain text password
        :return: hashed password
        """
        return self.pwd_context.hash(password)
