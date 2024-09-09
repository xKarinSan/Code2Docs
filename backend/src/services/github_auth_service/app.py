from fastapi import FastAPI
from src.services.github_auth_service.routes import router

github_auth_service_app = FastAPI()
github_auth_service_app.include_router(router)
