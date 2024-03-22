from fastapi import APIRouter, HTTPException
from api.project_api.task.schemas import TaskCreateSchema, TaskUpdateSchema, TaskResponseSchema
from api.project_api.dependencies import current_user_id, task_service
from sqlalchemy.exc import IntegrityError
from fastapi import Depends
import uuid
from models.models import User
from api.user_api.dependencies import get_current_user
router = APIRouter(prefix="/projects", tags=["Tasks"])


@router.post("/{project_id}/new-task/")
async def create_task(
    database: task_service,
    data: TaskCreateSchema,
    project_id: int,
    user: User = Depends(get_current_user)

):
    try:
        if user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.create_task(
                session=database.session,
                project_id=project_id,
                user=user,
                message=data.message,
                url=data.url
                )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")


@router.patch("/tasks/{task_id}/")
async def updated_task(
    database: task_service,
    task_id: int,
    data: TaskUpdateSchema,
    user: User = Depends(get_current_user)
):
    try:
        if user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        data = data.model_dump()
        async with database.session.begin():
            response = await database.update_task(
                session=database.session,
                task_id=task_id,
                owner=user,
                data=data,
                )
            return TaskResponseSchema.model_validate(response)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
    
@router.delete("/tasks/{task_id}/delete")
async def delete_task(
    task_id: int,
    database: task_service,
    user: User = Depends(get_current_user)
):
    try:
        if user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.delete_task(
                session=database.session,
                task_id=task_id,
                owner=user
            )
            return response
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
    
@router.get("/tasks/{task_id}")
async def get_task(
    task_id: int,
    database: task_service,
    user: User = Depends(get_current_user)
    ):
    try:
        if user.is_authenticated == False:
            raise HTTPException(status_code=403, detail='user account is not verified')
        async with database.session.begin():
            response = await database.get_task(
                session=database.session,
                task_id=task_id,
                owner=user)
            return TaskResponseSchema.model_validate(response)
    except IntegrityError as err:
        raise HTTPException(status_code=503, detail=f"Database error: {err}")