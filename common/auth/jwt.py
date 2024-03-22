from datetime import datetime
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from .settings import JWTSettings
from fastapi import Response
from jose import jwt, JWTError
import uuid
from models.models import User
from fastapi import Response
from global_settings import SECRET_KEY


    

def create_token(data: dict, expiration_delta: timedelta):
    encoded_data = data.copy()
    expire_date = datetime.utcnow() + expiration_delta
    encoded_data.update({"exp": expire_date})
    encoded_jwt = jwt.encode(encoded_data, SECRET_KEY,  algorithm='HS256')
    return encoded_jwt