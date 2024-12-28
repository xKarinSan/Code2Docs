import sys

sys.path.append("../")
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.src.services.document_service.app import document_service_app
from backend.src.services.github_service.app import github_service_app
from backend.src.services.codebase_service.app import codebase_service_app
from backend.src.services.db_service.db import Base, engine
from mangum import Mangum

import uvicorn

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/demo", document_service_app)
app.mount("/doc", document_service_app)
app.mount("/gh", github_service_app)
app.mount("/codebase", codebase_service_app)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    # uvicorn.run("main:app", port=8000, reload=True)

handler = Mangum(app)
