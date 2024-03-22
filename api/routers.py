from .user_api.handlers import router as user_router
from .user_api.auth.login import router as login_router
from .tariff_api.handlers import router as tariff_router
from .project_api.project.handlers import router as project_router
from .project_api.task.handlers import router as task_router
from .user_api.auth.logout import router as logout_router

all_routers = [user_router, login_router,project_router, tariff_router, task_router,logout_router]