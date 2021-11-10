import jwt  # used for encoding and decoding jwt tokens
from fastapi import HTTPException  # used to handle error handling
from datetime import datetime, timedelta  # used to handle expiry time for tokens


class Auth:
    # to get a new secret key this run:
    # openssl rand -hex 32
    SECRET_KEY = "967e64e52668340468d3075c80461de8b22f484487be1fe83c8bd77c2ca06e79"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ALGORITHM = 'HS256'

    def encode_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                return payload['sub']
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def encode_refresh_token(self, username):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS, hours=0),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': username
        }
        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def refresh_token(self, refresh_token):
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                username = payload['sub']
                new_token = self.encode_token(username)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')

    def get_token_expiry(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM],  # We do not want an exception, when
                                 options={"verify_exp": False})  # the expiration is in the past
            scope = payload['scope']
            if scope == 'access_token' or scope == 'refresh_token':
                return datetime.utcfromtimestamp(payload['exp'])
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
