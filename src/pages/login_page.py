from src.pages.base_page import BasePage
import allure

class LoginPage(BasePage):
    """
    Page Object containing locators and specific actions for the Login and Registration.
    """

    # Locators
    EMAIL_INPUT = "[data-test='email']"
    PASSWORD_INPUT = "[data-test='password']"
    LOGIN_BTN = "[data-test='login-submit']"
    REGISTER_LINK = "[data-test='register-link']"
    
    # Registration Locators
    FIRST_NAME_INPUT = "[data-test='first-name']"
    LAST_NAME_INPUT = "[data-test='last-name']"
    DOB_INPUT = "[data-test='dob']"
    STREET_INPUT = "[data-test='street']"
    POSTCODE_INPUT = "[data-test='postal_code']"
    CITY_INPUT = "[data-test='city']"
    STATE_INPUT = "[data-test='state']"
    PHONE_INPUT = "[data-test='phone']"
    REGISTER_BTN = "[data-test='register-submit']"

    def navigate_login(self):
        """Goes directly to the login page."""
        self.navigate("/auth/login")

    @allure.step("Logging in with {email}")
    def login(self, email: str, password: str) -> None:
        """Fills the login form and submits."""
        self.fill_input(self.EMAIL_INPUT, email)
        self.fill_input(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BTN)
        # Wait for the login to complete (e.g., navigation to home or account page)
        self.page.wait_for_load_state("networkidle")

    @allure.step("Registering a new user")
    def register(self, user_data: dict) -> None:
        """Completes the registration form."""
        self.click_element(self.REGISTER_LINK)
        
        self.fill_input(self.FIRST_NAME_INPUT, user_data["first_name"])
        self.fill_input(self.LAST_NAME_INPUT, user_data["last_name"])
        self.fill_input(self.DOB_INPUT, user_data["dob"])
        self.fill_input(self.STREET_INPUT, user_data["address"]["street"])
        self.fill_input(self.POSTCODE_INPUT, user_data["address"]["postal_code"])
        self.fill_input(self.CITY_INPUT, user_data["address"]["city"])
        self.fill_input(self.STATE_INPUT, user_data["address"]["state"])
        self.fill_input(self.PHONE_INPUT, user_data["phone"])
        self.fill_input(self.EMAIL_INPUT, user_data["email"])
        self.fill_input(self.PASSWORD_INPUT, user_data["password"])
        
        self.click_element(self.REGISTER_BTN)
        self.page.wait_for_load_state("networkidle")
