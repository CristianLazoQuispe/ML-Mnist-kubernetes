from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
import shutil
from core.domain import PredictionResponse
from app.config.settings import IMAGES_DIR
from app.adapter.preprocess import preprocess_image
from app.adapter.model_runner import OnnxPredictionService
import time
router = APIRouter()
model = OnnxPredictionService(str(IMAGES_DIR.parent / "mnist-8.onnx"))

@router.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """Endpoint to predict the class of a given image.
    Args:
        file (UploadFile): The image file to be processed.
    Returns:
        PredictionResponse: The predicted class, probabilities, and time elapsed.
    """
    try:
        start = time.time()
        temp_path = IMAGES_DIR / f"{uuid.uuid4()}.jpg"
        with temp_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        img_tensor = preprocess_image(str(temp_path))
        pred, probs = model.predict(img_tensor)
        temp_path.unlink()
        time_elapsed = time.time() - start
        return PredictionResponse(predicted_class=pred, probabilities=probs,time_elapsed=time_elapsed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# health check endpoint
@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Service is running"}