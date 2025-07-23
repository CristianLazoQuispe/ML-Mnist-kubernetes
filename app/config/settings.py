from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = PROJECT_DIR / "assets" / "mnist-8.onnx"
IMAGES_DIR = PROJECT_DIR / "assets" / "test_images"
