from playwright.sync_api import APIRequestContext
from typing import Dict, Any

class ApiClient:
    """
    Wrapper around Playwright's APIRequestContext.
    Used for setting up test data and bypassing UI login.
    """

    def __init__(self, request_context: APIRequestContext):
        self.request = request_context

    def register_user(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Registers a new user via API and returns the response."""
        response = self.request.post("/users/register", data=payload)
        
        # We assert here to ensure setup didn't fail before UI tests even begin
        assert response.ok, f"Failed to register user: {response.status} {response.text()}"
        return response.json()

    def login(self, email: str, password: str) -> str:
        """
        Authenticates a user and returns the JWT access token.
        This is critical for Hybrid tests to inject into LocalStorage.
        """
        payload = {
            "email": email,
            "password": password
        }
        
        response = self.request.post("/users/login", data=payload)
        assert response.ok, f"Failed to login via API: {response.text()}"
        
        data = response.json()
        assert "access_token" in data, "No access_token found in login response"
        return data["access_token"]
        
    def add_to_cart(self, product_id: str) -> None:
        """Adds a product to the cart via API (requires authentication context)"""
        payload = {
            "product_id": product_id,
            "quantity": 1
        }
        response = self.request.post("/carts", data=payload)
        # 201 Created
        assert response.status == 201, f"Failed to add to cart: {response.text()}"
