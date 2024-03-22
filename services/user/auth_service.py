from common.database.base_service import BaseDataBaseService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from models.models import User
from common.utils.hashing import verify_password
from fastapi import  HTTPException, status
from .settings import UserDatabaseSettings

class AuthService(BaseDataBaseService):
    
    
    async def authenticate_user(
        self,
        session: AsyncSession,
        form_data: OAuth2PasswordRequestForm
    ):
        stmt = select(User).where(User.email == form_data.username)
        user = await session.execute(stmt)
        user = user.scalar_one_or_none()
        if user:
            if not verify_password(form_data.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password"
                    )
            return user
        else:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
            )
    
def get_auth_service():
    settings = UserDatabaseSettings()
    return AuthService(dsn=settings.db_dsn)