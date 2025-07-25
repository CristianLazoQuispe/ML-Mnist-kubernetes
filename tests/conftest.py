import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--api-url",
        action="store",
        default="http://localhost:8000/predict",
        help="URL base del API a testear",
    )


@pytest.fixture
def api_url(request):
    """Fixture to provide the API URL for tests."""
    return request.config.getoption("--api-url")


# From local machine
#pytest tests/ --api-url=http://localhost:8000/predict -v

# From Kubernetes cluster
#pytest tests/ --api-url=http://mnist-service:8000/predict -v
