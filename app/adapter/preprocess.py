from PIL import Image
import numpy as np

def preprocess_image(file_path: str) -> np.ndarray:
    """Preprocess the image for model prediction.
    Args:
        file_path (str): Path to the image file.
    Returns:
        np.ndarray: Preprocessed image tensor.
    """
    img = Image.open(file_path).convert("L").resize((28, 28))
    img_np = np.array(img).astype(np.float32) / 255.0
    img_np = img_np[np.newaxis, np.newaxis, :, :]  # shape (1,1,28,28)
    return img_np
