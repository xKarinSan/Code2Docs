from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.services.document_service.routes import router

document_service_app = FastAPI()
document_service_app.include_router(router)
document_service_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
