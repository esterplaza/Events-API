import pytest
from models import User


def test_user_password_hashing():
    """Test that password hashing and checking works correctly"""
    # Arrange: Create a user
    user = User(username="testuser")
    user.set_password("mypassword123")

    # Act & Assert: Check correct password
    assert user.check_password("mypassword123") == True

    # Act & Assert: Check wrong password
    assert user.check_password("wrongpassword") == False

    # Act & Assert: Check that password hash is stored (not plain text)
    assert user.password_hash != "mypassword123"
    assert user.password_hash is not None