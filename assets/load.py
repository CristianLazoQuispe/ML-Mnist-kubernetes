import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep, time
from pathlib import Path
import argparse
import statistics
import threading

# Argument parser to receive the endpoint URL
#URL = "http://mnist.local/predict" (when minikube tunnel is used and ingress is configured)
#URL = "http://localhost:8000/predict" (when running locally without Kubernetes or tunnel without ingress)

parser = argparse.ArgumentParser(description="Send MNIST image requests to an API endpoint.")
parser.add_argument("--url", type=str, required=True, help="Endpoint URL, e.g. http://localhost:8000/predict")
args = parser.parse_args()
URL = args.url

# Path to the image that will be sent
IMG = Path("assets/test_images/mnist_03.png")

# Shared counters and response time list
success_count = 0
fail_count = 0
response_times = []
lock = threading.Lock()  # Used to avoid race conditions when updating counters

# Log file path
LOG_FILE = Path("assets/log_results.txt")

def send_request():
    global success_count, fail_count
    start_time = time()
    try:
        with open(IMG, "rb") as f:
            files = {"file": ("mnist_03.png", f, "image/png")}
            # timeout is set to 5 seconds to avoid hanging requests
            # Adjust this value based on your API's expected response time
            response = requests.post(URL, files=files, timeout=5)
            elapsed = time() - start_time

            with lock:
                if response.status_code == 200:
                    success_count += 1
                    response_times.append(elapsed)
                else:
                    fail_count += 1
                    response_times.append(elapsed)
    except Exception as e:
        elapsed = time() - start_time
        with lock:
            fail_count += 1
            response_times.append(elapsed)

if __name__ == "__main__":
    #python3 assets/load.py --url=http://mnist.local/predict 

    total_requests = 2000
    max_workers = 50

    # Clean previous logs
    LOG_FILE.write_text("")

    print(f"Starting load test with {total_requests} requests...")
    start_global = time()

    # Use a thread pool to send requests concurrently
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request) for _ in range(total_requests)]
        for future in as_completed(futures):
            pass  # Wait for all threads to complete

    duration = time() - start_global

    # Compute statistics
    avg_time = statistics.mean(response_times)
    std_time = statistics.stdev(response_times) if len(response_times) > 1 else 0
    min_time = min(response_times)
    max_time = max(response_times)

    # Prepare summary
    summary = f"""
=== Load Test Summary ===
Total Requests: {total_requests}
Successes: {success_count}
Failures: {fail_count}
Total Time: {duration:.2f} seconds

Response Time (in seconds):
  Mean:    {avg_time:.4f}
  StdDev:  {std_time:.4f}
  Min:     {min_time:.4f}
  Max:     {max_time:.4f}
"""

    print(summary)

    # Write log to file
    with LOG_FILE.open("a") as log_file:
        log_file.write(summary)
