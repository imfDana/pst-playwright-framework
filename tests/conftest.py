import os
import pytest
import allure
from playwright.sync_api import sync_playwright, Playwright, Page
from faker import Faker
import json

from src.utils.config import Config
from src.api.api_client import ApiClient
from src.pages.home_page import HomePage
from src.pages.checkout_page import CheckoutPage
from src.pages.login_page import LoginPage

fake = Faker()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture the result of each test step.
    This allows us to know if a test failed and take action (like a screenshot).
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(autouse=True)
def screenshot_on_failure(request, page: Page):
    """
    Fixture that automatically takes a screenshot if a test fails
    and attaches it to the Allure report.
    """
    yield
    # request.node is the "item" from the hook above
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        try:
            screenshot_path = f"screenshots/{request.node.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            allure.attach.file(
                screenshot_path,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

@pytest.fixture(scope="session")
def context(playwright: Playwright):
    """
    Sets up the default browser context (headless mode according to config).
    We use scope="session" to avoid opening/closing the browser for every test if possible,
    but Playwright typically manages contexts per test. For a portfolio, per-test context is cleaner.
    """
    browser = playwright.chromium.launch(headless=Config.HEADLESS)
    context = browser.new_context(base_url=Config.BASE_UI_URL)
    yield context
    context.close()
    browser.close()

@pytest.fixture
def page(context):
    """
    Overrides the default Playwright page fixture to ensure every test 
    gets a fresh page with the correct base_url configured.
    """
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def api(playwright: Playwright):
    """
    Provides an APIRequestContext configured with the BASE_API_URL.
    """
    request_context = playwright.request.new_context(base_url=Config.BASE_API_URL)
    api_client = ApiClient(request_context)
    yield api_client
    request_context.dispose()

@pytest.fixture
def random_user():
    """Generates random user data using Faker."""
    # Generating a unique password to avoid the 'data leak' validation rule
    unique_password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True) + "A1!xZ"
    
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "password": unique_password,
        "dob": "1990-01-01",
        "phone": "5555555555",
        "address": {
            "street": fake.street_address(),
            "city": fake.city(),
            "state": fake.state(),
            "country": fake.country_code(),
            "postal_code": fake.postcode()
        }
    }

@pytest.fixture
def authenticated_context(playwright: Playwright, api, random_user):
    """
    The "Magic" fixture.
    Registers a user via API, logs them in via API, and injects the JWT token 
    into a fresh browser context's LocalStorage.
    """
    # 1. API Setup: Register User
    api.register_user(random_user)

    # 2. API Setup: Login and get Token
    token = api.login(random_user["email"], random_user["password"])

    # 3. UI Setup: Create browser context with injected LocalStorage state
    browser = playwright.chromium.launch(headless=Config.HEADLESS)
    
    # We construct a fake storage state dict matching Playwright's format
    # In PST, authentication is usually managed via localStorage
    # We must ensure we navigate to the domain first before injecting local storage, 
    # or use Playwright's init_script.
    
    context = browser.new_context(base_url=Config.BASE_UI_URL)
    
    # Navigate briefly to the base URL so we can set localStorage for that origin
    page = context.new_page()
    page.goto(Config.BASE_UI_URL)
    
    # Inject token into localStorage (assuming PST uses a specific key like 'auth-token')
    # We will assume a generic implementation, but this might need adjustment based on the exact app.
    page.evaluate(f"window.localStorage.setItem('auth-token', '{token}')")
    
    # Close the temporary page, the context now holds the state
    page.close()

    yield context
    context.close()
    browser.close()

# Page Object Fixtures
@pytest.fixture
def home_page(page):
    return HomePage(page)

@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)

@pytest.fixture
def login_page(page):
    return LoginPage(page)
