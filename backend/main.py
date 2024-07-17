from fastapi import FastAPI
from src.services.document_service.app import document_service_app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"Hello": "World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/document", document_service_app)

if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app)
