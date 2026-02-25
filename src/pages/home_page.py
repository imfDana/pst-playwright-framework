from src.pages.base_page import BasePage
import allure

class HomePage(BasePage):
    """
    Page Object containing locators and specific actions for the Practice Software Testing Home Page.
    """

    # Locators
    CATEGORY_CHECKBOX = "label[data-test='category-01HXGBFR231WXZZ9CYS3Q1RPYV']"  # Hand Tools
    PRICE_SLIDER = "input[data-test='price-slider']"
    PRODUCT_CARD = "a[data-test^='product-']"

    def navigate_home(self):
        """Goes directly to the home grid."""
        self.navigate("/")

    @allure.step("Filtering by 'Hand Tools' category")
    def filter_by_hand_tools(self) -> None:
        """Clicks the 'Hand Tools' category checkbox."""
        # A more generic approach would use text, but data-test is safer
        # Assuming 'Hand Tools' checkbox label is the one above
        self.click_element("text=Hand Tools")

    @allure.step("Setting price slider to {target_price}")
    def filter_by_price(self, target_price: int) -> None:
        """
        Simulates adjusting the price slider. 
        Note: True sliders require bounding box math. For simplicity here, we simulate a click on the track.
        """
        # Simple approximation for demonstration: 
        # In a real scenario you would evaluate Javascript to change the value or use bounding boxes.
        self.page.evaluate(f"document.querySelector('{self.PRICE_SLIDER}').value = {target_price}")
        # Trigger 'input' and 'change' events to let Angular catch it
        self.page.evaluate(f"document.querySelector('{self.PRICE_SLIDER}').dispatchEvent(new Event('input'))")
        self.page.evaluate(f"document.querySelector('{self.PRICE_SLIDER}').dispatchEvent(new Event('change'))")

    @allure.step("Counting visible products")
    def get_product_count(self) -> int:
        """Returns the number of products currently visible in the grid."""
        # Wait for any potential API call that refreshes the grid to settle
        self.page.wait_for_timeout(1000) # Small implicit wait to allow Angular digest 
        count = self.page.locator(self.PRODUCT_CARD).count()
        return count
