from fastapi import FastAPI
from app.api.endpoints import router
import uvicorn

app = FastAPI(
    title="MNIST FastAPI ONNX Service",
    description="MNIST image classification service using FastAPI and ONNX.",
    version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
