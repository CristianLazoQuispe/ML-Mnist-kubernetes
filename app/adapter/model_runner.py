import onnxruntime as ort
import numpy as np
from core.service import PredictionService

class OnnxPredictionService(PredictionService):
    def __init__(self, model_path: str):
        providers = ["CUDAExecutionProvider", "CPUExecutionProvider"]
        self.session = ort.InferenceSession(model_path, providers=providers)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def predict(self, image: np.ndarray):
        outputs = self.session.run([self.output_name], {self.input_name: image})[0]
        probabilities = outputs[0]
        predicted_class = int(np.argmax(probabilities))
        return predicted_class, probabilities.tolist()
