import requests
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from pathlib import Path

IMG = Path("assets/test_images/mnist_03.png")
# activar primero el tunnel (el ingress ya mapea a mnist.local)
URL = "http://mnist.local/predict"

def send_request():
    with open(IMG, "rb") as f:
        files = {"file": ("mnist_03.png", f, "image/png")}
        try:
            r = requests.post(URL, files=files, timeout=5)
            print(r.status_code, r.json())
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=50) as executor:
        for _ in range(2000):
            executor.submit(send_request)
            sleep(0.01)
