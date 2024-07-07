from fastapi import FastAPI
from services.document_service.routes import router

document_service_app = FastAPI()
document_service_app.include_router(router)
