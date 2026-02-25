import pytest
import allure
from playwright.sync_api import Page, expect

@allure.feature("Search Functionality")
@allure.story("Product Search and Results Validation")
@pytest.mark.ui
def test_search_functionality(page: Page, home_page):
    """
    Test Case: Search for a specific product.
    Validates that the search bar returns relevant results.
    """
    with allure.step("1. Navigate to Home Page"):
        home_page.navigate_home()

    with allure.step("2. Search for a product"):
        search_input = page.locator("[data-test='search-query']")
        search_input.fill("Pliers")
        search_input.press("Enter")

    with allure.step("3. Validate search results"):
        # Wait for results to load
        page.wait_for_load_state("networkidle")
        
        # Check that results are visible
        product_cards = page.locator(home_page.PRODUCT_CARD)
        count = product_cards.count()
        
        assert count > 0, "No products found for search query 'Pliers'"
        
        # Verify at least one product contains "Pliers" in the title
        first_product_title = product_cards.first.locator(".card-title").inner_text()
        assert "pliers" in first_product_title.lower(), f"Expected 'pliers' in title, got {first_product_title}"
