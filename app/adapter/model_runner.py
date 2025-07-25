import onnxruntime as ort
import numpy as np
from core.service import PredictionService

class OnnxPredictionService(PredictionService):
    """Service for running predictions using an ONNX model.
    This class uses ONNX Runtime to load the model and perform inference.
    Args:
        model_path (str): Path to the ONNX model file.
    Attributes:
        session (onnxruntime.InferenceSession): The ONNX Runtime session for the model.
        input_name (str): Name of the input tensor for the model.
        output_name (str): Name of the output tensor for the model.
    """
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
