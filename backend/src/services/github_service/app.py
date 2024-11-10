from fastapi import FastAPI, Request
from backend.src.services.github_service.routes import router
import time

github_service_app = FastAPI()
github_service_app.include_router(router)
