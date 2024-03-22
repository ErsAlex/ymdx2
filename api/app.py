from fastapi import FastAPI
from fastapi import APIRouter
from api.routers import all_routers

def create_app():
    app = FastAPI(
        debug=True,
        docs_url="/api/docs",
        title="Kv_yndx_FastApi"
        )
    for router in all_routers:
        app.include_router(router)
    return app