from fastapi import FastAPI
from services.document_service.app import document_service_app
import uvicorn

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"Hello": "World"}


app.mount("/document", document_service_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
