def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="http://localhost:8000/predict",
        help="URL base del API a testear",
    )

import pytest

@pytest.fixture
def api_url(request):
    return request.config.getoption("--api-url")


# Desde tu laptop
#pytest tests/ --api-url=http://localhost:8000/predict -v

# Desde Kubernetes tester pod
#pytest tests/ --api-url=http://mnist-service:8000/predict -v
