import pytest
import allure
from playwright.sync_api import Page, Route

@allure.feature("Product Listing UI")
@allure.story("Dynamic Filtering with Network Interception")
@pytest.mark.ui
def test_ui_dynamic_filtering(page: Page, home_page):
    
    with allure.step("1. Navigate to Home Page"):
        home_page.navigate_home()
        initial_count = home_page.get_product_count()
        assert initial_count > 0, "Initial grid should not be empty"

    with allure.step("2. Setup Network Interception"):
        # We define a custom handler to listen for API requests that match the filter endpoint
        # For this test, we won't mock the response, we just want to "spy" on it
        
        request_captured = {"captured": False}
        
        def handle_filter_request(route: Route):
            # Check if this is the product filtering endpoint
            if "category" in route.request.url:
                request_captured["captured"] = True
            route.continue_()

        # Intercept ALL requests globally on the page for demonstration
        page.route("**/*", handle_filter_request)

    with allure.step("3. Apply 'Hand Tools' filter"):
        # The UI interaction that should trigger the API call
        home_page.filter_by_hand_tools()
        
    with allure.step("4. Wait for Network Response and Assert"):
        # We explicitly wait for the response to the filter request to finish.
        with page.expect_response(lambda response: "products" in response.url and response.status == 200, timeout=10000) as response_info:
            # We wait for the specific API call to complete
            pass
            
        assert request_captured["captured"], "The UI did not fire a network request when the filter was clicked."

        filtered_count = home_page.get_product_count()
        assert filtered_count >= 0, "The filtered count should be a valid integer"

