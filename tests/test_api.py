import pytest
import requests
import time
from tests.conftest import BASE_URL


def test_health_check():
    """Test that the health endpoint returns healthy status"""
    # Act: Make request to health endpoint
    response = requests.get(url=f"{BASE_URL}/health")

    # Assert: Check status code
    assert response.status_code == 200

    # Assert: Check response body
    data = response.json()
    assert data["status"] == "healthy"


def test_register_user_creates_new_user():
    """Test that user registration"""
    username = f"testuser_{int(time.time())}"
    user_data = {
        "username": username,
        "password": "testpassword"
    }

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    assert response.status_code == 201

    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == username


def test_login_returns_jwt_token():
    """Test that login returns jwt_token"""
    username = f"testuser_{int(time.time())}"
    user_data = {
        "username": username,
        "password": "testpassword"
    }

    requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )

    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=user_data
    )

    assert response.status_code == 200

    auth_data = response.json()
    assert "access_token" in auth_data
    assert auth_data["user"]["username"] == username


def test_create_public_event_requires_auth_and_succeeds_with_token(auth_token):
    """Test creating a public event"""
    # Arrange: Event data
    event_data = {
      "title": "Python Meetup",
      "description": "Monthly Python developer meetup",
      "date": "2026-01-15T18:00:00",
      "location": "Tech Hub, Room 101",
      "capacity": 50,
      "is_public": True,
      "requires_admin": False
    }

    # Act: Create Event
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )

    # Assert: Check response
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]
    assert data["date"] == event_data["date"]
    assert data["location"] == event_data["location"]
    assert data["capacity"] == event_data["capacity"]
    assert data["is_public"] == True
    assert data["requires_admin"] == False
    assert "id" in data


def test_double_user_registration():
    """Test double user registration"""
    username = f"testuser_{int(time.time())}"
    user_data = {
        "username": username,
        "password": "testpassword"
    }

    first_response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    assert first_response.status_code == 201

    double_response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    assert double_response.status_code == 400


def test_create_public_event_without_token():
    """Test creating a public event without token"""
    # Arrange: Event data
    event_data = {
      "title": "Python Meetup",
      "description": "Monthly Python developer meetup",
      "date": "2026-01-15T18:00:00",
      "location": "Tech Hub, Room 101",
      "capacity": 50,
      "is_public": True,
      "requires_admin": False
    }

    # Act: Create Event
    response = requests.post(
        f"{BASE_URL}/events",
        json=event_data
    )

    # Assert: Check response
    assert response.status_code == 401


def test_rsvp_to_public_event(auth_token):
    """Test creating an rsvp to a public event"""
    username = f"testuser_{int(time.time())}"
    user_data = {
        "username": username,
        "password": "testpassword"
    }

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    data_user = response.json()
    user_id = data_user["user"]["id"]

    event_data = {
        "title": "Public Test Event",
        "date": "2026-10-15T18:00:00",
        "is_public": True
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    event_response = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )
    assert event_response.status_code == 201

    event = event_response.json()
    event_id = event["id"]
    rsvp_data = {
        "event_id": event_id,
        "user_id": user_id,
        "attending": True
    }
    response = requests.post(
        f"{BASE_URL}/rsvps/event/{event_id}",
        json = rsvp_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["event_id"] == event_id
    assert data["attending"] is True


def test_rsvp_to_a_not_public_event_without_authorization(auth_token):
    """Test creating an rsvp to a not public event without authorization"""
    username = f"testuser_{int(time.time())}"
    user_data = {
        "username": username,
        "password": "testpassword"
    }

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=user_data
    )
    data_user = response.json()
    user_id = data_user["user"]["id"]

    event_data = {
        "title": "Not Public Test Event",
        "date": "2026-10-15T18:00:00",
        "is_public": False
    }
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    event_response = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )
    assert event_response.status_code == 201

    event = event_response.json()
    event_id = event["id"]
    rsvp_data = {
        "event_id": event_id,
        "user_id": user_id,
        "attending": True
    }
    response = requests.post(
        f"{BASE_URL}/rsvps/event/{event_id}",
        json=rsvp_data
    )
    assert response.status_code == 401






