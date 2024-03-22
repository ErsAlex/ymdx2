from typing import Annotated
from fastapi import Depends
from common.auth.rest import get_user_id_from_token
from services.project.project_service import ProjectDatabaseService, get_project_service
from services.task.task_service import TaskDatabaseService, get_task_service
from fastapi import Request, Path



task_service = Annotated[TaskDatabaseService, Depends(get_task_service)]
project_service = Annotated[ProjectDatabaseService, Depends(get_project_service)]
current_user_id = Annotated[str, Depends(get_user_id_from_token)]