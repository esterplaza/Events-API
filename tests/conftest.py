import pytest
import requests
import time

# BaseURL for API tests
BASE_URL = "http://localhost:5000/api"

@pytest.fixture
def base_url():
    """Fixture providing the base URL for API tests"""
    return BASE_URL

@pytest.fixture
def auth_token():
    """Fixture that registers a user and returns auth token"""
    # Create unique username using timestamp
    timestamp = int(time.time() * 1000)
    username = f"testuser_{timestamp}"

    # Register user
    user_data = {
        "username": username,
        "password": "testpass123"
    }

    requests.post(url=f"{BASE_URL}/auth/register", json=user_data)

    # Login and get token
    response = requests.post(f"{BASE_URL}/auth/login", json=user_data)
    token = response.json()["access_token"]

    return token
