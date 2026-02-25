import pytest
import allure
from playwright.sync_api import Page, expect

@allure.feature("Shopping Cart")
@allure.story("Add Product to Cart")
@pytest.mark.ui
def test_add_to_cart(page: Page, home_page):
    """
    Test Case: Add a product to the shopping cart.
    Validates that the cart counter updates correctly.
    """
    with allure.step("1. Navigate to Home Page"):
        home_page.navigate_home()

    with allure.step("2. Click on first product"):
        product_1 = page.locator(home_page.PRODUCT_CARD).first
        product_1.click()
        page.wait_for_load_state("networkidle")

    with allure.step("3. Add product to cart"):
        page.locator("[data-test='add-to-cart']").click()
        
        # Wait for cart counter to update
        expect(page.locator("[data-test='cart-quantity']")).to_have_text("1")
        
    with allure.step("4. Verify product was added"):
        # Check that the cart quantity badge is showing 1
        cart_badge = page.locator("[data-test='cart-quantity']")
        expect(cart_badge).to_have_text("1")
