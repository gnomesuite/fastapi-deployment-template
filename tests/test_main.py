"""
Test cases for the Pet Store API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Pet Store API is running!"
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_get_pets():
    """Test getting all pets"""
    response = client.get("/pets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3  # We have 3 sample pets

def test_get_pets_with_filters():
    """Test getting pets with status filter"""
    response = client.get("/pets?status=available")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for pet in data:
        assert pet["status"] == "available"

def test_get_pet_by_id():
    """Test getting a specific pet by ID"""
    response = client.get("/pets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Buddy"

def test_get_nonexistent_pet():
    """Test getting a non-existent pet"""
    response = client.get("/pets/999")
    assert response.status_code == 404
    assert "Pet not found" in response.json()["detail"]

def test_create_pet():
    """Test creating a new pet"""
    pet_data = {
        "name": "Fluffy",
        "category": "cat",
        "status": "available",
        "tags": ["cute", "fluffy"],
        "price": 199.99,
        "description": "A fluffy white cat",
        "photo_urls": ["https://example.com/fluffy1.jpg"]
    }
    response = client.post("/pets", json=pet_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == pet_data["name"]
    assert data["category"] == pet_data["category"]
    assert data["price"] == pet_data["price"]
    assert "id" in data
    assert "created_at" in data

def test_update_pet():
    """Test updating an existing pet"""
    update_data = {
        "name": "Buddy Updated",
        "price": 349.99
    }
    response = client.put("/pets/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]

def test_delete_pet():
    """Test deleting a pet"""
    # First create a pet to delete
    pet_data = {
        "name": "Test Pet",
        "category": "dog",
        "status": "available",
        "tags": ["test"],
        "price": 99.99,
        "description": "A test pet"
    }
    create_response = client.post("/pets", json=pet_data)
    pet_id = create_response.json()["id"]
    
    # Then delete it
    response = client.delete(f"/pets/{pet_id}")
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify it's deleted
    get_response = client.get(f"/pets/{pet_id}")
    assert get_response.status_code == 404

def test_get_orders():
    """Test getting all orders"""
    response = client.get("/orders")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_order():
    """Test creating a new order"""
    order_data = {
        "pet_id": 1,
        "user_id": 1,
        "quantity": 1,
        "status": "placed"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 201
    data = response.json()
    assert data["pet_id"] == order_data["pet_id"]
    assert data["user_id"] == order_data["user_id"]
    assert data["quantity"] == order_data["quantity"]

def test_create_order_invalid_pet():
    """Test creating an order with invalid pet ID"""
    order_data = {
        "pet_id": 999,
        "user_id": 1,
        "quantity": 1
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400
    assert "Pet not found" in response.json()["detail"]

def test_get_users():
    """Test getting all users"""
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # We have 2 sample users

def test_create_user():
    """Test creating a new user"""
    user_data = {
        "username": "newuser",
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@example.com",
        "password": "password123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]

def test_create_user_duplicate_username():
    """Test creating a user with duplicate username"""
    user_data = {
        "username": "johndoe",  # This already exists
        "first_name": "John",
        "last_name": "Doe",
        "email": "john2@example.com",
        "password": "password123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 400
    assert "Username already exists" in response.json()["detail"]

def test_get_inventory():
    """Test getting inventory"""
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "available" in data
    assert "sold" in data

def test_pagination():
    """Test pagination parameters"""
    response = client.get("/pets?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2

def test_validation_errors():
    """Test validation errors"""
    # Test with invalid data
    invalid_pet = {
        "name": "",  # Empty name should fail
        "price": -10,  # Negative price should fail
    }
    response = client.post("/pets", json=invalid_pet)
    assert response.status_code == 422  # Validation error