from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"Hello": "World"}


if __name__ == "__main__":
    uvicorn.run("main:main_app", host="0.0.0.0", port=8000, reload=True)
