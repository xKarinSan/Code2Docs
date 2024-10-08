from fastapi import FastAPI, Request
from src.services.document_service.app import document_service_app
from src.services.github_service.app import github_service_app
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"message": "Hello World"}

@app.middleware("http")
async def test_middleware(request: Request, call_next):
    print("i'm  triggered")
    response = await call_next(request)
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/demo", document_service_app)
app.mount("/gh", github_service_app)

if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app)
