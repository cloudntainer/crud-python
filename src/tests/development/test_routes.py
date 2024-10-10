import pytest
from flask import Flask
from src.api.routes import main_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(main_bp)

    with app.test_client() as client:
        yield client


@pytest.fixture
def test_data():
    return [
        {"name": "Item 1"},
        {"name": "Item 2"},
        {"name": "Item 3"}
    ]


def test_index(client):
    response = client.get('/')
    if response.status_code != 200:
        raise Exception(
            "Expected status code 200, got {}".format(response.status_code)
        )
    if b'Welcome to the API!' not in response.data:
        raise Exception("Expected message not found in response data")


def test_get_items(client, test_data):
    response = client.get('/api/items')
    if response.status_code != 200:
        raise Exception(
            "Expected status code 200, got {}".format(response.status_code)
        )
    if len(
        response.get_json(
        )
    ) != len(
        test_data
    ):
        raise Exception(
            "Expected item count {}, got {}".format(len(test_data),
                                                    len(response.get_json()))
        )


def test_get_item(client):
    response = client.get('/api/items/1')
    if response.status_code != 200:
        raise Exception(
            "Expected status code 200, got {}".format(response.status_code)
        )
    if response.get_json(
    )[
        'name'
    ] != "Item 2":
        raise Exception(
            "Expected item name 'Item 2', got {}".format(
                response.get_json(
                )[
                    'name'
                ]
            )
        )


def test_get_item_not_found(client):
    response = client.get('/api/items/10')
    if response.status_code != 404:
        raise Exception(
            "Expected status code 404, got {}".format(response.status_code)
        )


def test_add_item(client):
    new_item = {"name": "New Item"}
    response = client.post('/api/items', json=new_item)
    if response.status_code != 201:
        raise Exception(
            "Expected status code 201, got {}".format(response.status_code)
        )
    if b'Item added successfully' not in response.data:
        raise Exception("Expected success message not found in response data")


def test_add_existing_item(client):
    existing_item = {"name": "Item 1"}
    response = client.post('/api/items', json=existing_item)
    if response.status_code != 400:
        raise Exception(
            "Expected status code 400, got {}".format(response.status_code)
        )
    if b'Item already exists' not in response.data:
        raise Exception("Expected error message not found in response data")


def test_update_item(client):
    updated_item = {"name": "Updated Item"}
    response = client.put('/api/items/1', json=updated_item)
    if response.status_code != 200:
        raise Exception(
            "Expected status code 200, got {}".format(response.status_code)
        )
    if b'Item updated successfully' not in response.data:
        raise Exception(
            "Expected success message not found in response data"
        )


def test_delete_item(client):
    response = client.delete('/api/items/1')
    if response.status_code != 200:
        raise Exception(
            "Expected status code 200, got {}".format(response.status_code)
        )
    if b'Item deleted successfully' not in response.data:
        raise Exception(
            "Expected success message not found in response data"
        )


def test_delete_item_not_found(client):
    response = client.delete('/api/items/10')
    if response.status_code != 404:
        raise Exception(
            "Expected status code 404, got {}".format(response.status_code)
        )
