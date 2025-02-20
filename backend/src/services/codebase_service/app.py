from fastapi import FastAPI
from src.services.codebase_service.routes import router

codebase_service_app = FastAPI()
codebase_service_app.include_router(router)
