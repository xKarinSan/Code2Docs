import sys

sys.path.append("../")
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.services.doc_gen_service.app import doc_gen_service_app
from src.services.github_service.app import github_service_app
from src.services.codebase_service.app import codebase_service_app
from src.services.docs_service.app import docs_service_app
from src.services.db_service.db import Base, engine
from mangum import Mangum

# add the schemas
from src.services.db_service.models import DocModel, DocSetModel, CodebaseModel
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

app.mount("/demo", doc_gen_service_app)
app.mount("/docgen", doc_gen_service_app)
app.mount("/gh", github_service_app)
app.mount("/codebase", codebase_service_app)
app.mount("/docs", docs_service_app)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    # uvicorn.run("main:app", port=8000, reload=True)

handler = Mangum(app)
