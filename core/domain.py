# core/domain.py

from pydantic import BaseModel
from typing import List

class PredictionRequest(BaseModel):
    filename: str

class PredictionResponse(BaseModel):
    predicted_class: int
    probabilities: List[float]
