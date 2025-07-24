import requests
import os
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "assets" / "test_images"
URL = "http://localhost:8000/predict"

for image_path in IMAGES_DIR.glob("*.png"):
    with open(image_path, "rb") as f:
        files = {"file": (image_path.name, f, "image/jpeg")}
        response = requests.post(URL, files=files)
        print(f"{image_path.name} → {response.json()}")
