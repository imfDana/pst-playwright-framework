import pytest
import allure
from src.api.api_client import ApiClient

@allure.feature("Authentication API")
@allure.story("User Registration and Login flow")
@pytest.mark.api
def test_api_registration_and_login(api: ApiClient, random_user: dict):
    """
    Test Case 1: API Testing.
    Demonstrates ability to test backend systems without relying on UI.
    """

    with allure.step("1. Register a new user via POST /users/register"):
        response = api.register_user(random_user)
        assert response is not None, "Registration response should not be empty"

    with allure.step("2. Authenticate the newly created user via POST /users/login"):
        token = api.login(random_user["email"], random_user["password"])

    with allure.step("3. Validate the JWT token structure"):
        assert isinstance(token, str), "Token must be a string"
        assert len(token) > 20, "Token is suspiciously short for a JWT"

