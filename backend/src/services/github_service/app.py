from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.src.services.github_service.routes import router
import time

github_service_app = FastAPI()
github_service_app.include_router(router)
github_service_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
