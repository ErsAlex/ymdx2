from fastapi.routing import APIRouter
from api.user_api.dependencies import get_current_user
from api.tariff_api.dependencies import tariff_service
from .schemas import AddTariffSchema, UpdateTariffSchema
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from models.models  import User
from fastapi import Depends
from fastapi import HTTPException

router = APIRouter(tags=["tariffs"])


@router.post("/add")
async def add_tariff_to_user(
    database: tariff_service,
    tariff: AddTariffSchema,
    current_user: User = Depends(get_current_user)
    ):
    try:
        if current_user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.add_tariff_to_user(
            session=database.session,
            user=current_user,
            tariff=tariff.tariff
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@router.patch("/update")
async def udpdate_user_tariff(
    database: tariff_service,
    tariff: UpdateTariffSchema,
    current_user: User = Depends(get_current_user)
    ):
    try:
        if current_user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.change_user_tariff(
            session=database.session,
            user=current_user,
            new_tariff=tariff.tariff
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    

@router.delete("/delete")
async def delete_user_tariff(
    database: tariff_service,
    current_user: User = Depends(get_current_user)
    ):
    try:
        if current_user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.cancel_tariff(
            session=database.session,
            user=current_user,
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")