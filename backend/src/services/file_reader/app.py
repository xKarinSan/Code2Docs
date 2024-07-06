from fastapi import FastAPI
from services.file_reader.routes import router

file_reader_app = FastAPI()
file_reader_app.include_router(router)
