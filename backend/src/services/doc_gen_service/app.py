from fastapi import FastAPI
from src.services.doc_gen_service.routes import router

doc_gen_service_app = FastAPI()
doc_gen_service_app.include_router(router)
