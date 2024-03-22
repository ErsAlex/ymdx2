from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from .settings import JWTSettings
from jose import jwt, JWTError
import uuid
from .utils import OAuth2PasswordBearerWithCookie

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login")



async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    try:
        settings = JWTSettings()
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
            )
        data: str = payload.get('sub')
        if data is None:
            raise exeption
    except JWTError:
        raise exeption
    user_id = data
    return user_id
 
async def get_user_data_from_token(token: str = Depends(oauth2_scheme)):
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    try:
        settings = JWTSettings()
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
            )
        if payload is None:
            raise exeption
    except JWTError:
        raise exeption
    return payload