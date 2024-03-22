from common.database.base_service import BaseDataBaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from common.database.base_service import BaseDataBaseService
from models.models import Project, Tariff, UserTariff, Task,  User
import uuid
from .settings import TaskDatabaseSettings
from fastapi import HTTPException

class TaskDatabaseService(BaseDataBaseService):
    def __init__(self, settings: TaskDatabaseSettings):
        super().__init__(dsn=settings.db_dsn)
        self._settings = settings
        
    async def create_task(
        self,
        session: AsyncSession,
        project_id: int,
        user: User,
        message: str,
        url: str,
        ):
        
        stmt = select(Tariff).join(UserTariff).filter(UserTariff.user_id==user.id)
        tariff = await session.execute(stmt)
        tariff = tariff.scalar_one_or_none()
        
        stmt = select(Task).filter(Task.owner_id == user.id)
        result = await session.execute(stmt)
        user_tasks = result.scalars().all()
        if tariff.task_limit <= len(user_tasks):
            return {'response': "user already have max number of tasks"}

        task = Task(
            message=message,
            owner_id=user.id,
            project_id=project_id,
            url=url
            )
        session.add(task)
        await session.commit()
        return {"response": "Task created successfully"}
    
    
    async def delete_task(
        self,
        session: AsyncSession,
        task_id: int,
        owner: User
        ):
        
        task_stmt = select(Task).where(Task.id==task_id)
        task = await session.execute(task_stmt)
        task = task.scalar_one_or_none()
        if task.owner_id != owner.id:
            raise HTTPException(status_code=403, detail=f"Access denied")
        stmt = delete(Task).where(Task.id==task_id)
        await session.execute(stmt)
        return {"response": "task was deleted"}
    
    
    async def update_task(
        self,
        session: AsyncSession,
        task_id: int,
        data: dict,
        owner: User
        ):
        
        task_stmt = select(Task).where(Task.id==task_id)
        task = await session.execute(task_stmt)
        task = task.scalar_one_or_none()
        if task.owner_id != owner.id:
            raise HTTPException(status_code=403, detail=f"Access denied")
        stmt = update(Task).where(Task.id==task_id).values(**data).returning(Task)
        updated_task = await session.execute(stmt)
        updated_task = updated_task.scalar_one_or_none()
        return updated_task
    
    async def get_task(
        self,
        session: AsyncSession,
        task_id: int,
        owner: User
        ):
        
        task_stmt = select(Task).where(Task.id==task_id)
        task = await session.execute(task_stmt)
        task = task.scalar_one_or_none()
        if task.owner_id != owner.id:
            raise HTTPException(status_code=403, detail=f"Access denied")

        return task
    
    
    
    
def get_task_service():
    return TaskDatabaseService(
        settings=TaskDatabaseSettings()
        )