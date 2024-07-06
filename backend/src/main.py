from fastapi import FastAPI
from services.file_reader.app import file_reader_app
import uvicorn

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    return {"Hello": "World"}


app.mount("/file_reader", file_reader_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
