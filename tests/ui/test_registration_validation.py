import pytest
import allure
from playwright.sync_api import Page, expect

@allure.feature("User Authentication")
@allure.story("Login Validation - Wrong Password")
@pytest.mark.ui
def test_login_wrong_password(page: Page, home_page):
    """
    Test Case: Try to login with an incorrect password.
    Validates that the system shows an appropriate error message.
    """
    with allure.step("1. Navigate to Login Page"):
        page.goto("/auth/login")
        page.wait_for_load_state("networkidle")

    with allure.step("2. Attempt login with wrong password"):
        page.locator("[data-test='email']").fill("customer@practicesoftwaretesting.com")
        page.locator("[data-test='password']").fill("wrongpassword123!")
        page.locator("[data-test='login-submit']").click()

    with allure.step("3. Validate error message is displayed"):
        # Wait for error toast or message
        page.wait_for_timeout(2000)
        error_message = page.locator(".alert-danger, .help-block")
        
        # Assert error is visible
        expect(error_message.first).to_be_visible(timeout=5000)
