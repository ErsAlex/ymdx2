from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from common.database.base_service import BaseDataBaseService
from common.utils.hashing import get_password_hash
from common.utils.key_generator import codegen
from models.models import User, Tariff, UserTariff, UserSecretKeys
from .settings import UserDatabaseSettings
import uuid
from fastapi import HTTPException
from common.utils.hashing import verify_password
from sqlalchemy import text
from services.email.email_service import EmailBody, send_email

class UserDatabaseService(BaseDataBaseService):

    async def create_user(
    self,
    session: AsyncSession,
    user_name: str, 
    user_surname: str,
    password1: str,
    password2: str,
    email: str,
    ):  
        if password1 != password2:
             raise HTTPException(
                    status_code=403,
                    detail="passwords dont't match"
                    )
        new_user = User(
        user_name = user_name,
        user_surname = user_surname,
        email = email,
        password = get_password_hash(password1)
        )
        key = codegen(6)
        user_key = UserSecretKeys(
            email = new_user.email,
            key_type = "AUTH_KEY",
            key=get_password_hash(key)
        )
        session.add_all([new_user, user_key])
        await session.commit()
        print(key)
        
        email = EmailBody(
            to=new_user.email,
            subject='Registration code',
            message=f'Your registartion code is {key}')
        
        
        #await send_email(body=email)

        return new_user
    
    async def get_account_validation_code(
        self,
        session: AsyncSession,
        user: User,
        
        ):
        user_key_stmt = select(UserSecretKeys).where(UserSecretKeys.email == user.email)
        user_key = await session.execute(user_key_stmt)
        user_key = user_key.scalar_one_or_none()
        key = codegen(6)
        hasded_key = get_password_hash(key)
        stmt = update(UserSecretKeys).where(UserSecretKeys.email==user.email).values(key=hasded_key)
        await session.execute(stmt)
        
        email = EmailBody(
            to=user.email,
            subject='Registration code',
            message=f'Your registartion code is {key}')
        
        
        #await send_email(body=email)
        print(key)
        return {"response": "new code was sent on your email"}

    async def user_account_validation(
        self,
        session: AsyncSession,
        user: User,
        secret_key:str
    ):
        user_key_stmt = select(UserSecretKeys).where(UserSecretKeys.email == user.email)
        user_key = await session.execute(user_key_stmt)
        user_key = user_key.scalar_one_or_none()
        if user_key.key_type != "AUTH_KEY" or not verify_password(secret_key, user_key.key):
            raise HTTPException(
                    status_code=403,
                    detail="Wrong Code"
                    )
        else:
            update_query = text("UPDATE kv_users SET is_authenticated = true WHERE id = :user_id")
            delete_query = text("DELETE FROM kv_keys WHERE email = :email")


            await session.execute(update_query, {"user_id": user.id})
            await session.execute(delete_query, {"email": user.email})

            await session.commit()
            return {"response": f"user {user.id} account is confirmed"}
    
    
    async def get_password_reset_key(
        self,
        session: AsyncSession,
        email: str,
    ):
        user_stmt = select(User).where(User.email==email)
        user = await session.execute(user_stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                    status_code=403,
                    detail="User not found"
                    )
        key = codegen(6)
        user_secret_key = UserSecretKeys(
            user_id = user.id,
            key_type="PASS_RESET_KEY",
            key=get_password_hash(key),
        )
        session.add(user_secret_key)
        await session.commit()
        
        email = EmailBody(
            to=user.email,
            subject='Passsword reset',
            message=f'Your password reset code is {key}')
        
        print(key)
        #await send_email(body=email)
    
        return {"message":"Password reset code was sent on your email adress"}
    
    
    async def update_user(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        data: dict,
    ):
        stmt = update(User).where(User.id==user_id).values(**data).returning(User)
        updated_user = await session.execute(stmt)
        updated_user = updated_user.scalar_one_or_none()
        return updated_user
    
    async def get_temporary_password(
        self,
        session: AsyncSession,
        email: str,
        secret_key: str
    ):
        user_stmt = select(User).where(User.email==email)
        user = await session.execute(user_stmt)
        user = user.scalar_one_or_none()
        if not user:
            raise HTTPException(
                    status_code=403,
                    detail="User not found"
                    )
        user_key_stmt = select(UserSecretKeys).where(UserSecretKeys.user_id == user.id)
        user_key = await session.execute(user_key_stmt)
        user_key = user_key.scalar_one_or_none()
        if user_key.key_type != "PASS_RESET_KEY" or not verify_password(secret_key, user_key.key):
            raise HTTPException(
                    status_code=403,
                    detail="Wrong Code"
                    )
        temp_password = codegen(8)
        temp_password_hash = get_password_hash(temp_password)
        stmt = update(User).where(User.id==user.id).values(password=temp_password_hash)
        del_stmt = delete(UserSecretKeys).where(UserSecretKeys.user_id==user.id)
        await session.execute(stmt)
        await session.execute(del_stmt)
        email = EmailBody(
            to=user.email,
            subject='New password',
            message=f'Your temporay password is  {temp_password}')
        
        print(temp_password)
        #await send_email(email)
        return {"response": "temporary password was sent on your email , please login and make new password"}
        
        
    async def password_update(
        self,
        session: AsyncSession,
        user_id: uuid.UUID,
        old_password: str,
        new_password: str
    ):
        
        user_stmt = select(User).where(User.id == user_id)

        user = await session.execute(user_stmt)
        user = user.scalar_one_or_none()
        if not verify_password(old_password, user.password):
                raise HTTPException(
                    status_code=401,
                    detail="Incorrect password"
                    )
        password = get_password_hash(new_password)
        stmt = update(User).where(User.id==user_id).values(password=password)
        await session.execute(stmt)
        return {"response": "password updated successfully"}
        
    async def get_user(
        self,
        session: AsyncSession,
        **filter_by
    ):            
        stmt = select(User).filter_by(**filter_by)
        user = await session.execute(stmt)
        user = user.scalar_one_or_none()
        return user
    
    async def get_user_tariff(
        self,
        session: AsyncSession,
        user_id: uuid.UUID
    ):
        stmt = select(Tariff).join(UserTariff).filter(UserTariff.user_id==user_id)
        tariff = await session.execute(stmt)
        tariff = tariff.scalar_one_or_none()
        return tariff
        
    async def delete_user(
        self,
        session: AsyncSession,
        **filter_by
    ):
        stmt = delete(User).filter_by(**filter_by)
        await session.execute(stmt)
        return {"user_deleted": True}
        

    
    
        
def get_user_service():
    settings = UserDatabaseSettings()
    return UserDatabaseService(dsn=settings.db_dsn)