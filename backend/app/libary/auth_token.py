import jwt  # used for encoding and decoding jwt tokens
from fastapi import HTTPException  # used to handle error handling
from datetime import datetime, timedelta  # used to handle expiry time for tokens


class AuthToken:
    def __init__(self):
        # To get a new secret key this run:
        # openssl rand -hex 32
        self.SECRET_KEY = "967e64e52668340468d3075c80461de8b22f484487be1fe83c8bd77c2ca06e79"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 15
        self.REFRESH_TOKEN_EXPIRE_DAYS = 7
        self.ALGORITHM = 'HS256'
        self.COOKIE_MAX_AGE = self.REFRESH_TOKEN_EXPIRE_DAYS*24*60*60

    def encode_access_token(self, user_id):
        """
        Creates an access token with signature.
        :param user_id: unique id of the user (can be string or integer)
        :return: JSON Web Token (JWT)
        """
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES),
            'iat': datetime.utcnow(),
            'scope': 'access_token',
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def decode_access_token(self, token):
        """
        Decodes an access token, and verifies if the token is valid.
        :param token: the access token
        :return: subject claim (user_id)
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                return payload['sub']
            raise HTTPException(status_code=401, detail='Scope for the access token is invalid')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Access token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid access token')

    def encode_refresh_token(self, user_id):
        """
        Encodes an refresh token with signature.
        :param user_id: unique id of the user (can be string or integer)
        :return JSON Web Token (JWT)
        """
        payload = {
            'exp': datetime.utcnow() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS, hours=0),
            'iat': datetime.utcnow(),
            'scope': 'refresh_token',
            'sub': user_id
        }
        return jwt.encode(
            payload,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def decode_refresh_token(self, token):
        """
        Decodes an refresh token, and verifies if the token is valid.
        :param token: the refresh token
        :return: subject claim (user_id)
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                return payload['sub']
            raise HTTPException(status_code=401, detail='Invalid scope for refresh token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid refresh token')

    def get_token_expiry(self, token):
        """
        Decodes both access/refresh tokens, and verifies if the token is valid.
        This function does not verify the Expiration Time Claim (exp).
        :param token: the access token or refresh token
        :return: a UTC datetime
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM],
                                 options={"verify_exp": False})
            # verify_exp to False. We do not want an exception if the JWT is expired
            scope = payload['scope']
            if scope == 'access_token' or scope == 'refresh_token':
                return datetime.utcfromtimestamp(payload['exp'])
            raise HTTPException(status_code=401, detail='Scope for the token is invalid')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
