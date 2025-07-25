# core/domain.py

from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    """Request model for image prediction.
    Attributes:
        filename (str): Name of the image file.
    """
    filename: str

class PredictionResponse(BaseModel):
    """Response model for prediction results.
    Attributes:
        predicted_class (int): The predicted class label.
        probabilities (List[float]): List of probabilities for each class.
        time_elapsed (float): Time taken for the prediction in seconds.
    """
    predicted_class: int
    probabilities: List[float]
    time_elapsed: float