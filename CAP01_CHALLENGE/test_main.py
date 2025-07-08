import pytest
from fastapi.testclient import TestClient
from main import app, fake_db, SECRET_KEY, ALGORITHM
import jwt
from passlib.context import CryptContext

client = TestClient(app)

# Test data
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass"
TEST_NUMBERS = [5, 2, 8, 1, 9]
SORTED_TEST_NUMBERS = sorted(TEST_NUMBERS)
TEST_EVEN_NUMBERS = [2, 8]
TEST_SUM = sum(TEST_NUMBERS)
TEST_MAX = max(TEST_NUMBERS)
TEST_TARGET = 8
TEST_TARGET_INDEX = SORTED_TEST_NUMBERS.index(TEST_TARGET)
NON_EXISTENT_TARGET = 99

@pytest.fixture(autouse=True)
def clear_db_before_tests():
    """Clear the fake DB before each test"""
    fake_db["users"].clear()
    yield

def get_auth_token():
    """Helper function to register a user and get an auth token"""
    # Register user
    client.post("/register", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    # Login to get token
    response = client.post("/login", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    return response.json()["access_token"]

def test_register_user_success():
    """Test successful user registration"""
    response = client.post("/register", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}
    assert TEST_USERNAME in fake_db["users"]
    assert CryptContext(schemes=["bcrypt"]).verify(TEST_PASSWORD, fake_db["users"][TEST_USERNAME])

def test_register_existing_user():
    """Test registering an existing user"""
    # First registration
    client.post("/register", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    # Second registration attempt
    response = client.post("/register", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

def test_login_success():
    """Test successful login"""
    # Register first
    client.post("/register", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    # Then login
    response = client.post("/login", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    # Verify token is valid
    token = response.json()["access_token"]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == TEST_USERNAME

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    # Register first
    client.post("/register", params={"username": TEST_USERNAME, "password": TEST_PASSWORD})
    
    # Wrong password
    response = client.post("/login", params={"username": TEST_USERNAME, "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
    
    # Wrong username
    response = client.post("/login", params={"username": "wronguser", "password": TEST_PASSWORD})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"

def test_protected_endpoints_without_token():
    """Test that protected endpoints return 401 without a valid token"""
    endpoints = [
        ("/sum", {"numbers": TEST_NUMBERS}),
        ("/bubble-sort", {"numbers": TEST_NUMBERS}),
        ("/filter-even", {"numbers": TEST_NUMBERS}),
        ("/max-value", {"numbers": TEST_NUMBERS}),
        ("/binary-search", {"numbers": SORTED_TEST_NUMBERS, "target": TEST_TARGET}),
    ]
    
    for endpoint, payload in endpoints:
        response = client.post(endpoint, json=payload)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid authentication credentials"

def test_protected_endpoints_with_invalid_token():
    """Test that protected endpoints return 401 with an invalid token"""
    invalid_token = "invalid.token.here"
    headers = {"Authorization": f"Bearer {invalid_token}"}
    
    endpoints = [
        ("/sum", {"numbers": TEST_NUMBERS}),
        ("/bubble-sort", {"numbers": TEST_NUMBERS}),
        ("/filter-even", {"numbers": TEST_NUMBERS}),
        ("/max-value", {"numbers": TEST_NUMBERS}),
        ("/binary-search", {"numbers": SORTED_TEST_NUMBERS, "target": TEST_TARGET}),
    ]
    
    for endpoint, payload in endpoints:
        response = client.post(endpoint, json=payload, headers=headers)
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid authentication credentials"

def test_sum_numbers_success():
    """Test the sum endpoint with valid input"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/sum", params={"token": token}, json={"numbers": TEST_NUMBERS}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"sum": TEST_SUM}

def test_sum_numbers_empty_list():
    """Test the sum endpoint with empty list"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/sum", params={"token": token}, json={"numbers": []}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "List of numbers cannot be empty"

def test_bubble_sort_success():
    """Test the bubble sort endpoint with valid input"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/bubble-sort", params={"token": token}, json={"numbers": TEST_NUMBERS}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"sorted_numbers": SORTED_TEST_NUMBERS}

def test_bubble_sort_empty_list():
    """Test the bubble sort endpoint with empty list"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/bubble-sort", params={"token": token}, json={"numbers": []}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "List of numbers cannot be empty"

def test_filter_even_numbers_success():
    """Test the filter even numbers endpoint with valid input"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/filter-even", params={"token": token}, json={"numbers": TEST_NUMBERS}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"even_numbers": TEST_EVEN_NUMBERS}

def test_filter_even_numbers_empty_list():
    """Test the filter even numbers endpoint with empty list"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/filter-even", params={"token": token}, json={"numbers": []}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "List of numbers cannot be empty"

def test_max_value_success():
    """Test the max value endpoint with valid input"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/max-value", params={"token": token}, json={"numbers": TEST_NUMBERS}, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"max": TEST_MAX}

def test_max_value_empty_list():
    """Test the max value endpoint with empty list"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/max-value", params={"token": token}, json={"numbers": []}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "List of numbers cannot be empty"

def test_binary_search_success_found():
    """Test the binary search endpoint when target is found"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {"numbers": SORTED_TEST_NUMBERS, "target": TEST_TARGET}
    response = client.post("/binary-search", params={"token": token}, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"found": True, "index": TEST_TARGET_INDEX}

def test_binary_search_success_not_found():
    """Test the binary search endpoint when target is not found"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    payload = {"numbers": SORTED_TEST_NUMBERS, "target": NON_EXISTENT_TARGET}
    response = client.post("/binary-search", params={"token": token}, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"found": False, "index": -1}

def test_binary_search_empty_list():
    """Test the binary search endpoint with empty list"""
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/binary-search", params={"token": token}, json={"numbers": [], "target": TEST_TARGET}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "List of numbers cannot be empty"