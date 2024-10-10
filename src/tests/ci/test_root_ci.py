import requests
from requests_mock import Mocker


BASE_URL = "http://localhost:5000"


def test_endpoint_status():
    with Mocker() as m:
        m.get(f"{BASE_URL}/endpoint", status_code=200)
        response = requests.get(f"{BASE_URL}/endpoint", timeout=5)

        if response.status_code != 200:
            raise ValueError(
                "Expected status code 200,"
                f"got {response.status_code}"
            )

        if not m.called:
            raise RuntimeError("Mock request was not called")

        request = m.request_history[0]
        if request.url != f"{BASE_URL}/endpoint":
            raise ValueError(
                f"Expected request URL {BASE_URL}/endpoint,"
                f"got {request.url}"
            )
