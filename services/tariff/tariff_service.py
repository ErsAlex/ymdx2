from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from common.database.base_service import BaseDataBaseService
from common.utils.hashing import get_password_hash
from models.models import User, Tariff, UserTariff
from .settings import TariffDatabaseSettings






class TariffDatabaseService(BaseDataBaseService):
    async def add_tariff_to_user(
    self,
    session: AsyncSession,
    user: User,
    tariff: str
    ):  

        new_tariff_stmt = select(Tariff).where(Tariff.tariff_name == tariff)
        new_tariff = await session.execute(new_tariff_stmt)
        new_tariff = new_tariff.scalar_one_or_none()

        new_user_tariff = UserTariff(
            user_id=user.id,
            tariff=new_tariff
        )
        session.add(new_user_tariff)
        await session.commit()
        return {"respose": f"Tariff '{new_tariff.tariff_name}' added to user {user.id}"}

    async def change_user_tariff(
    self,
    session: AsyncSession,
    user: User,
    new_tariff: str 
    ):
        
        new_tariff_stmt = select(Tariff).where(Tariff.tariff_name == new_tariff)
        new_tariff = await session.execute(new_tariff_stmt)
        new_tariff = new_tariff.scalar_one_or_none()

        stmt = update(UserTariff).where(UserTariff.user_id==user.id).values(tariff_id=new_tariff.id)
        await session.execute(stmt)
        return {"respose": f"Tariff changed to '{new_tariff.tariff_name}"}
    
    async def cancel_tariff(
        self,
        session: AsyncSession,
        user: User,
    ):
        stmt = delete(UserTariff).where(UserTariff.user_id==user.id)
        await session.execute(stmt)
        return {'response': "Tariff canceled"}



    async def get_tariff(
        self,
        session: AsyncSession,
        tariff: str
    ):
        get_tariff_stmt = select(Tariff).where(Tariff.tariff_name == tariff)
        tariff = await session.execute(get_tariff_stmt)
        tariff = tariff.scalar_one_or_none()
        return tariff
        


def get_tariff_service():
    settings = TariffDatabaseSettings()
    return TariffDatabaseService(dsn=settings.db_dsn)


