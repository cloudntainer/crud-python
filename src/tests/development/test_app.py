import logging
import pytest
from src.app import app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_log.txt"),
        logging.StreamHandler()
    ]
)


@pytest.fixture
def client():
    """Fixture to create a test client for the application."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_item(client):
    """Fixture to create a sample item for tests."""
    response = client.post('/api/items', json={'name': 'Sample Item'})
    check_status_code(response, 201)
    return response.json


def check_status_code(response, expected_code):
    """Verify that the response status code is as expected."""
    if response.status_code != expected_code:
        logging.error(
            f"Expected status code {expected_code}, "
            f"got {response.status_code}."
        )
        raise AssertionError(
            f"Expected status code {expected_code}, "
            f"got {response.status_code}."
        )
    logging.info(f"Test passed: Status code is {expected_code}.")


class TestAPI:
    def test_index(self, client):
        """Test the index route."""
        response = client.get('/')
        check_status_code(response, 200)

        if b'Welcome to the API!' not in response.data:
            logging.error("Welcome message not found in response.")
            raise AssertionError("Welcome message not found in response.")
        logging.info("Welcome message found in response.")

    def test_get_items(self, client):
        """Test to get all items."""
        response = client.get('/api/items')
        check_status_code(response, 200)

        if len(response.json) == 0:
            logging.error("Expected at least one item in the response.")
            raise AssertionError("Expected at least one item in the response.")
        logging.info("Get items response is valid and contains items.")

    def test_add_item(self, client):
        """Test to add a new item."""
        response = client.post('/api/items', json={'name': 'New Item'})
        check_status_code(response, 201)

        if b'Item added successfully' not in response.data:
            logging.error(
                "Item added successfully message not found in response."
            )
            raise AssertionError(
                "Item added successfully message not found in response."
            )
        logging.info(
            "Item added successfully message found in response."
        )

    def test_add_item_invalid(self, client):
        """Test to try adding an item with invalid data."""
        response = client.post('/api/items', json={'invalid_key': 'New Item'})
        check_status_code(response, 400)

        if b'Invalid data' not in response.data:
            logging.error("Invalid data error message not found in response.")
            raise AssertionError(
                "Invalid data error message not found in response."
            )
        logging.info(
            "Invalid data error message found in response."
        )

    def test_delete_item(self, client, sample_item):
        """Test to delete an item."""
        item_id = sample_item['id']
        response = client.delete(f'/api/items/{item_id}')
        check_status_code(response, 204)

        response = client.get(f'/api/items/{item_id}')
        check_status_code(response, 404)

    def test_update_item(self, client, sample_item):
        """Test to update an existing item."""
        item_id = sample_item['id']
        response = client.put(
            f'/api/items/{item_id}',
            json={'name': 'Updated Item'}
        )
        check_status_code(response, 200)

        response = client.get(f'/api/items/{item_id}')
        if b'Updated Item' not in response.data:
            logging.error("Updated Item not found in response.")
            raise AssertionError("Updated Item not found in response.")
        logging.info("Updated Item found in response.")

    def test_get_nonexistent_item(self, client):
        """Test to try getting a nonexistent item."""
        response = client.get('/api/items/9999')
        check_status_code(response, 404)

        if b'Item not found' not in response.data:
            logging.error("Item not found message not found in response.")
            raise AssertionError(
                "Item not found message not found in response."
            )
        logging.info(
            "Item not found message found in response."
        )

    def test_access_protected_route_without_auth(self, client):
        """Test to access a protected route without authentication."""
        response = client.get('/api/protected-route')
        check_status_code(response, 401)

        if b'Unauthorized' not in response.data:
            logging.error("Unauthorized message not found in response.")
            raise AssertionError("Unauthorized message not found in response.")
        logging.info("Unauthorized message found in response.")
