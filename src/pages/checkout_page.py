from src.pages.base_page import BasePage
import allure

class CheckoutPage(BasePage):
    """
    Page Object containing locators and specific actions for the Checkout flow.
    """

    # Locators
    PROCEED_1_BTN = "[data-test='proceed-1']"
    PROCEED_2_BTN = "[data-test='proceed-2']"
    PROCEED_3_BTN = "[data-test='proceed-3']"
    CONFIRM_BTN = "[data-test='finish']"
    SUCCESS_MESSAGE = ".help-block:has-text('Payment was successful')"

    # Form Locators
    ADDRESS_INPUT = "[data-test='street']"
    CITY_INPUT = "[data-test='city']"
    STATE_INPUT = "[data-test='state']"
    POSTCODE_INPUT = "[data-test='postal_code']"
    PAYMENT_METHOD_SELECT = "[data-test='payment-method']"

    def navigate_cart(self):
        """Goes directly to the cart page."""
        self.navigate("/cart")

    @allure.step("Completing step 1: Login Check")
    def complete_step_1(self) -> None:
        """Clicks proceed assuming user is already authenticated (Hybrid test)."""
        self.click_element(self.PROCEED_1_BTN)

    @allure.step("Completing step 2: Billing Address")
    def complete_step_2(self, address: str, city: str, state: str, country: str = None, postcode: str = None) -> None:
        """Fills out the billing address form and proceeds."""
        self.fill_input(self.ADDRESS_INPUT, address)
        self.fill_input(self.CITY_INPUT, city)
        self.fill_input(self.STATE_INPUT, state)
        if postcode:
            self.fill_input(self.POSTCODE_INPUT, postcode)
        self.click_element(self.PROCEED_2_BTN)

    @allure.step("Completing step 3: Payment Method")
    def complete_step_3(self, method: str = "Cash on Delivery") -> None:
        """Selects a payment method and proceeds."""
        self.page.locator(self.PAYMENT_METHOD_SELECT).select_option(label=method)
        self.click_element(self.PROCEED_3_BTN)

    @allure.step("Confirming Order")
    def confirm_order(self) -> None:
        """Clicks the final confirmation button."""
        self.click_element(self.CONFIRM_BTN)

    @allure.step("Validating Success Message")
    def validate_success(self) -> bool:
        """Checks if the success message is visible."""
        element = self.page.locator(self.SUCCESS_MESSAGE)
        element.wait_for(state="visible", timeout=10000)
        return element.is_visible()
