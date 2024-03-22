from pydantic_settings import BaseSettings
from datetime import timedelta
from global_settings import SECRET_KEY, ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE



class JWTSettings(BaseSettings):
    
    access_token_expires: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    refresh_token_expires: timedelta  = timedelta(minutes=REFRESH_TOKEN_EXPIRE)
    
    secret_key: str = SECRET_KEY
    
    algorithm: str = "HS256"