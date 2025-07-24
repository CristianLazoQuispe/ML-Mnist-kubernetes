import pytest
import requests
from pathlib import Path

# URL del servicio en contenedor local
#API_URL = "http://localhost:8000/predict"
API_URL = "http://ml-mnist-kube:8000/predict"
TEST_IMAGES_DIR = Path(__file__).resolve().parent.parent / "assets" / "test_images"

# Parsear el nombre del archivo para obtener la etiqueta
def get_label_from_filename(filename: str) -> int:
    # Soporta nombres como mnist_03.png
    digits = [int(s) for s in filename if s.isdigit()]
    return int("".join(map(str, digits))) if digits else -1

@pytest.mark.parametrize("img_path", TEST_IMAGES_DIR.glob("*.png"))
def test_prediction_correct(img_path):
    expected_label = get_label_from_filename(img_path.name)

    with open(img_path, "rb") as f:
        files = {"file": (img_path.name, f, "image/png")}
        response = requests.post(API_URL, files=files)

    assert response.status_code == 200, f"Error {response.status_code} on {img_path.name}"
    data = response.json()
    predicted = data["predicted_class"]

    assert predicted == expected_label, f"{img_path.name}: esperado {expected_label}, predicho {predicted}"
