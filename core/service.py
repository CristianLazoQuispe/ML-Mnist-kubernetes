from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np

class PredictionService(ABC):
    """Abstract base class for prediction services.
    This class defines the interface for prediction services that can be used
    """
    @abstractmethod
    def predict(self, image: np.ndarray) -> Tuple[int, np.ndarray]:
        pass
