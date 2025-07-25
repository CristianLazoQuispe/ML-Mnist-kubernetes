import pytest
import requests
from pathlib import Path

TEST_IMAGES_DIR = Path(__file__).resolve().parent.parent / "assets" / "test_images"

def get_label_from_filename(filename: str) -> int:
    digits = [int(s) for s in filename if s.isdigit()]
    return int("".join(map(str, digits))) if digits else -1

@pytest.mark.parametrize("img_path", TEST_IMAGES_DIR.glob("*.png"))
def test_prediction_correct(img_path, api_url):  # <-- use the api_url fixture
    """Test that the prediction API returns the expected class for each image.
    Inputs:
        img_path (Path): Path to the image file to be tested.
        api_url (str): The API URL to which the request will be sent. "http://localhost:8000/predict" or "http://ml-mnist-kube:8000/predict"
    """
    expected_label = get_label_from_filename(img_path.name)

    with open(img_path, "rb") as f:
        files = {"file": (img_path.name, f, "image/png")}
        response = requests.post(api_url, files=files)

    assert response.status_code == 200, f"Error {response.status_code} on {img_path.name}"
    data = response.json()
    predicted = data["predicted_class"]
    assert predicted == expected_label, f"{img_path.name}: esperado {expected_label}, predicho {predicted}"


    assert predicted == expected_label, f"{img_path.name}: esperado {expected_label}, predicho {predicted}"

# pytest tests/ --api-url=http://localhost:8000/predict -v
# pytest tests/ --api-url=http://ml-mnist-kube:8000/predict -v
