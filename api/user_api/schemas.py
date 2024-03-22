import uuid
from pydantic import BaseModel, ConfigDict, Field
from enum import Enum

class TariffEnum(str, Enum):
    Demo = "Demo"
    Full = "Full"

   
class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_name: str
    user_surname: str
    email: str
    is_authenticated: bool

class UserUpdateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: str

class UserCreateSchema(BaseModel):
    user_name: str
    user_surname: str
    email: str
    password1: str
    password2: str
    
class UserPasswordChangeSchema(BaseModel):
    old_password: str
    new_password: str
    
class UserSecretKeyInput(BaseModel):
    user_key: str