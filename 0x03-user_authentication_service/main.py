#!/usr/bin/env python3
"""
advanced tasks
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

def register_user(email: str, password: str) -> None:
    """
    Function to register a user via the corresponding endpoint.

    Args:
        email (str): The email address of the user to be registered.
        password (str): The password of the user to be registered.
    """
    response = requests.post("http://localhost:5000/users", data={"email": email, "password": password})
    assert response.status_code == 200, f"Registration failed: {response.json()}"

def log_in_wrong_password(email: str, password: str) -> None:
    """
    Function to attempt login with the wrong password via the corresponding endpoint.

    Args:
        email (str): The email address of the user.
        password (str): The incorrect password.
    """
    response = requests.post("http://localhost:5000/login", data={"email": email, "password": password})
    assert response.status_code == 401, f"Login with wrong password should fail: {response.json()}"

def log_in(email: str, password: str) -> str:
    """
    Function to log in a user via the corresponding endpoint.

    Args:
        email (str): The email address of the user.
        password (str): The password of the user.

    Returns:
        str: The session ID if login is successful.
    """
    response = requests.post("http://localhost:5000/login", data={"email": email, "password": password})
    assert response.status_code == 200, f"Login failed: {response.json()}"
    return response.json()["session_id"]

def profile_unlogged() -> None:
    """
    Function to check the profile of an unlogged user via the corresponding endpoint.
    """
    response = requests.get("http://localhost:5000/profile")
    assert response.status_code == 401, f"Accessing profile should be unauthorized: {response.json()}"

def profile_logged(session_id: str) -> None:
    """
    Function to check the profile of a logged-in user via the corresponding endpoint.

    Args:
        session_id (str): The session ID of the logged-in user.
    """
    response = requests.get("http://localhost:5000/profile", headers={"session_id": session_id})
    assert response.status_code == 200, f"Failed to access profile: {response.json()}"

def log_out(session_id: str) -> None:
    """
    Function to log out a user via the corresponding endpoint.

    Args:
        session_id (str): The session ID of the user to log out.
    """
    response = requests.post("http://localhost:5000/logout", headers={"session_id": session_id})
    assert response.status_code == 200, f"Logout failed: {response.json()}"

def reset_password_token(email: str) -> str:
    """
    Function to request a reset password token via the corresponding endpoint.

    Args:
        email (str): The email address of the user.

    Returns:
        str: The reset token.
    """
    response = requests.post("http://localhost:5000/reset_password", data={"email": email})
    assert response.status_code == 200, f"Failed to get reset token: {response.json()}"
    return response.json()["reset_token"]

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Function to update user password via the corresponding endpoint.

    Args:
        email (str): The email address of the user.
        reset_token (str): The reset token for password reset.
        new_password (str): The new password.
    """
    response = requests.post("http://localhost:5000/update_password", data={"email": email, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200, f"Failed to update password: {response.json()}"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
