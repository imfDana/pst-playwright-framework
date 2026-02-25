from playwright.sync_api import Page, expect
import allure

class BasePage:
    """
    Core page object containing shared methods for interacting with elements.
    It encapsulates Playwright's API to build more robust and readable tests.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "/") -> None:
        """Navigates to the specified relative path."""
        self.page.goto(path)
        self.page.wait_for_load_state("networkidle")

    def click_element(self, selector: str) -> None:
        """Clicks an element after ensuring it is visible and enabled."""
        element = self.page.locator(selector).first
        element.wait_for(state="visible")
        element.click()

    def fill_input(self, selector: str, text: str) -> None:
        """Fills an input field after clearing it."""
        element = self.page.locator(selector).first
        element.wait_for(state="visible")
        element.fill(text)
