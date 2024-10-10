import requests
import pytest

BASE_URL = "http://localhost:50010"


def test_endpoint_status():
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=10)
        if response.status_code != 200:
            print(f"Unexpected status code: {response.status_code}")
            pytest.fail(f"Unexpected status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        pytest.fail(f"Request failed: {e}")
