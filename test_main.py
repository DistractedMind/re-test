import pytest
from fastapi.testclient import TestClient
from main import app, items

client = TestClient(app)
test_item = {"id": 0, "name": "test_item", "description": "test_item_description"}
test_item_u = {"id": 0, "name": "test_item", "description": "test_item_description_u"}
test_item_1 = {"id": 1, "name": "test_item_1", "description": "test_item_description_1"}

@pytest.fixture(autouse=True)
def clear_items():
    items.clear()

def test_create_item_success(): #1
    response = client.post("/items/", json=test_item)
    assert response.status_code == 201, "Item creation should succeed."
    assert response.json() == test_item

def test_create_item_duplicate(): #2
    client.post("/items/", json=test_item)
    response = client.post("/items/", json=test_item)
    assert response.status_code == 400, "Duplicate item creation should fail."
    assert response.json()["detail"] == "Item already exists"

def test_get_items(): #3
    client.post("/items/", json=test_item)
    client.post("/items/", json=test_item_1)
    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    ids = [item["id"] for item in data.values()]
    assert 0 in ids and 1 in ids

def test_get_item_success(): #4
    client.post("/items/", json=test_item)
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == test_item
    
def test_get_item_not_found(): #5
    response = client.get("/items/0")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_update_item_success(): #6
    client.post("/items/", json=test_item)
    response = client.put("/items/0", json=test_item_u)
    assert response.status_code == 200
    assert response.json() == test_item_u

def test_update_item_not_found(): #7
    response = client.put("/items/0", json=test_item)
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_delete_item_success(): #8
    client.post("/items/", json=test_item)
    response = client.delete("/items/0")
    assert response.status_code == 204
    response = client.get("/items/0")
    assert response.status_code == 404

def test_delete_item_not_found(): #9
    response = client.delete("/items/0")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"
