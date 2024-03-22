from fastapi.routing import APIRouter
from .dependencies import user_service, get_current_user
from .schemas import UserCreateSchema, UserSchema, UserUpdateSchema, UserPasswordChangeSchema, UserSecretKeyInput
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException
from models.models  import User
from fastapi import Depends
from api.tariff_api.schemas import TariffSchema


router = APIRouter(tags=["users"])

@router.post("/")
async def create_user(
    database: user_service,
    user: UserCreateSchema
    ):
    try:
        async with database.session.begin():
            new_user = await database.create_user(
                session=database.session,
                user_name=user.user_name,
                user_surname=user.user_surname,
                email=user.email,
                password1=user.password1,
                password2=user.password2
                )
        return UserSchema.model_validate(new_user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.get('/me')
async def get_request_user(
    current_user: User = Depends(get_current_user)
    ):
    return UserSchema.model_validate(current_user)

@router.patch("/me")
async def update_user(
    database: user_service,
    updated_data: UserUpdateSchema,
    current_user: User = Depends(get_current_user)
    ):
    try:
        data = updated_data.model_dump()
        async with database.session.begin():
            user = await database.update_user(
            session=database.session,
            user_id=current_user.id,
            data=data
            )
            return UserSchema.model_validate(user)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
    
@router.patch("/me/password-update")
async def update_user_password(
    database: user_service,
    updated_data: UserPasswordChangeSchema,
    current_user: User = Depends(get_current_user)
    ):
    try:
        async with database.session.begin():
            response = await database.password_update(
            session=database.session,
            user_id=current_user.id,
            old_password=updated_data.old_password,
            new_password=updated_data.new_password
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
    
@router.post("/me/account-validate")
async def user_account_validation(
    database: user_service,
    user_key: UserSecretKeyInput,
    current_user: User = Depends(get_current_user)
    ):
    try:
        async with database.session.begin():
            response = await database.user_account_validation(
            session=database.session,
            user=current_user,
            secret_key=user_key.user_key
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.post("/me/reset-key")
async def get_password_reset_key(
    database: user_service,
    user_email: str,
    ):
    try:
        async with database.session.begin():
            response = await database.get_password_reset_key(
            session=database.session,
            email=user_email
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
    
    
@router.post("/me/password-reset")
async def get_temporary_password(
    database: user_service,
    user_email: str,
    user_key: UserSecretKeyInput
    ):
    try:
        async with database.session.begin():
            response = await database.get_temporary_password(
            session=database.session,
            email=user_email,
            secret_key=user_key.user_key
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
    
@router.get("/me/new-validation-code")
async def get_new_validation_code(
    database: user_service,
    current_user: User = Depends(get_current_user)
):
    try:
        async with database.session.begin():
            response = await database.get_account_validation_code(
            session=database.session,
            user=current_user
            
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    



@router.delete("/me")
async def delete_user(
    database: user_service,
    current_user: User = Depends(get_current_user)
    ):
    try:
        async with database.session.begin():
            response = await database.delete_user(
            database.session,
            id=current_user.id
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")

@router.get("/me/tariff")
async def get_user_tariff(
    database: user_service,
    current_user: User = Depends(get_current_user)
    
):
    try:
        async with database.session.begin():
            tariff = await database.get_user_tariff(
                database.session,
                user_id=current_user.id
            )
            return TariffSchema.model_validate(tariff)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")