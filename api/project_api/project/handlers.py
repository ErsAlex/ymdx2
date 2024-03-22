from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
import uuid
from models.models import User
from api.project_api.dependencies import project_service, current_user_id
from .schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectResponseSchema
from api.user_api.dependencies import get_current_user
router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("")
async def create_project(
    database: project_service,
    project_data: ProjectCreateSchema,
    owner: User = Depends(get_current_user)
    ):
    try:
        if owner.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.create_project(
                session=database.session,
                name=project_data.name,
                description=project_data.description,
                owner=owner,
                )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
@router.patch("/{project_id}/update")
async def update_project(
    data: ProjectUpdateSchema,
    project_id: int,
    database: project_service,
    owner: User = Depends(get_current_user)
):
    try:
        if owner.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        data = data.model_dump()
        async with database.session.begin():
            updated_project = await database.update_project(
                session=database.session,
                project_id=project_id,
                data=data,
                owner=owner
            )
            return ProjectResponseSchema.model_validate(updated_project)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.delete("/{project_id}/delete")
async def update_project(
    project_id: int,
    database: project_service,
    owner: User = Depends(get_current_user)
):
    try:
        if owner.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.delete_project(
                session=database.session,
                project_id=project_id,
                owner=owner
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
@router.get("/{project_id}")
async def get_project(
    project_id: int,
    database: project_service,
    owner: User = Depends(get_current_user)
    ):
    try:
        if owner.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.get_project(
                session=database.session,
                project_id=project_id,
                owner=owner)
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")