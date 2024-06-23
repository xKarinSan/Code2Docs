from fastapi import FastAPI
import uvicorn
from services.filehandler.routes import router as filehandler_router

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"Hello": "World"}


app.include_router(filehandler_router, prefix="/zip")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
