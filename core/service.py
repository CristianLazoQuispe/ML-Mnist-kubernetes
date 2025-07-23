from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np

class PredictionService(ABC):
    @abstractmethod
    def predict(self, image: np.ndarray) -> Tuple[int, np.ndarray]:
        pass
