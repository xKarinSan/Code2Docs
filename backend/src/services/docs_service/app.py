from fastapi import FastAPI
from src.services.docs_service.routes import router

docs_service_app = FastAPI()
docs_service_app.include_router(router)
