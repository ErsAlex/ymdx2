
from common.database.base_service import BaseDataBaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_
from common.database.base_service import BaseDataBaseService
from models.models import Project, Tariff, UserTariff, User
import uuid
from .settings import ProjectDatabaseSettings
from fastapi import HTTPException


class ProjectDatabaseService(BaseDataBaseService):
    def __init__(self, settings: ProjectDatabaseSettings):
        super().__init__(dsn=settings.db_dsn)
        self._settings = settings

    async def create_project(
        self,
        session: AsyncSession,
        name: str,
        description: str,
        owner: User
    ) -> Project:
        
        stmt = select(Tariff).join(UserTariff).filter(UserTariff.user_id==owner.id)
        tariff = await session.execute(stmt)
        tariff = tariff.scalar_one_or_none()
        if tariff.tariff_name not in ["Demo", "Full"]:
            return {"response": "user don't have tariff"}
        project = Project(
            name=name,
            description=description,
            owner_id=owner.id
            )
        session.add_all([project])
        return {"response": "project_created"}
    
    async def update_project(
        self,
        session: AsyncSession,
        project_id: int,
        data: dict,
        owner: User
        ):
        
        project_stmt = select(Project).where(Project.id==project_id)
        project = await session.execute(project_stmt)
        project = project.scalar_one_or_none()
        if project.owner_id != owner.id:
            raise HTTPException(status_code=403, detail=f"Access denied")
        stmt = update(Project).where(Project.id==project_id).values(**data).returning(Project)
        updated_project = await session.execute(stmt)
        updated_project = updated_project.scalar_one_or_none()
        return updated_project
    
    async def get_project(
        self,
        session: AsyncSession,
        project_id: int,
        owner: User
        ):
        
        project_stmt = select(Project).where(Project.id==project_id)
        project = await session.execute(project_stmt)
        project = project.scalar_one_or_none()
        if project.owner_id != owner.id:
            raise HTTPException(status_code=403, detail=f"Access denied")
        
        stmt = select(Project).where(Project.id==project_id)
        project = await session.execute(stmt)
        project = project.scalar_one_or_none()
        return project
    
    
    async def delete_project(
        self,
        session: AsyncSession,
        project_id: int,
        owner: User
        ):
        
        project_stmt = select(Project).where(Project.id==project_id)
        project = await session.execute(project_stmt)
        project = project.scalar_one_or_none()
        if project.owner_id != owner.id:
            raise HTTPException(status_code=403, detail=f"Access denied")
        
        
        stmt = delete(Project).where(Project.id==project_id)
        await session.execute(stmt)
        return {"response": f"project {project_id} was deleted"}
        
    
    
def get_project_service():
    return ProjectDatabaseService(settings=ProjectDatabaseSettings())