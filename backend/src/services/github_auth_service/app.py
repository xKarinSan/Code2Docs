from fastapi import FastAPI, Request
from src.services.github_auth_service.routes import router
import time

github_auth_service_app = FastAPI()
github_auth_service_app.include_router(router)
