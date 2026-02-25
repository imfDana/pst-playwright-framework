# Practice Software Testing - Playwright Framework

A robust, scalable, and modern E2E test automation framework built for portfolio demonstration.

This framework targets the [Practice Software Testing](https://practicesoftwaretesting.com/) application and demonstrates modern QA engineering practices using Playwright and Python.

## 🚀 Key Features

*   **Hybrid Testing (API + UI):** Bypasses slow UI steps (like login or cart setup) by using the REST API to inject state directly into the browser context. This reduces execution time by up to 80%.
*   **Page Object Model (POM):** Clean separation of UI locators/actions from test logic.
*   **Network Interception:** Uses `page.route()` to intercept and wait for specific network requests instead of using flaky `time.sleep()`.
*   **Data-Driven Generation:** Utilizes the `Faker` library to generate unique test data on the fly.
*   **CI/CD Integration:** Automated test execution and reporting via GitHub Actions.
*   **Allure Reporting:** Beautiful, highly detailed test reports.

## 🛠️ Technology Stack

*   **Language:** Python 3.13
*   **Framework:** Pytest & Pytest-Playwright
*   **Reporting:** Allure Reports
*   **Linter:** Ruff

## 📂 Project Structure

```text
├── .github/workflows/      # CI/CD pipelines (GitHub Actions)
├── src/
│   ├── api/                # API Client wrappers for state injection
│   ├── pages/              # Page Object Model classes
│   └── utils/              # Configuration and Environment variable handling
├── tests/
│   ├── api/                # API tests (Backend validation)
│   ├── ui/                 # UI tests (Network interception)
│   ├── hybrid/             # Hybrid tests (API Setup -> UI Validation)
│   └── e2e/                # Full End-to-End User Journeys
├── .env.example            # Environment variables template
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Python dependencies
```

## 💻 Getting Started

### 1. Prerequisites
*   Python 3.10+
*   Java (Required for generating Allure Reports locally)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/pst-playwright-framework.git
cd pst-playwright-framework

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
playwright install chromium --with-deps
```

### 3. Configuration
Copy `.env.example` to `.env` if you need to override the default URLs or configurations.
```bash
cp .env.example .env
```

## 🧪 Running Tests

**Run all tests:**
```bash
pytest
```

**Run specific test categories:**
```bash
pytest -m api       # Run only API tests
pytest -m ui        # Run only UI tests
pytest -m hybrid    # Run only Hybrid tests
pytest -m e2e       # Run only E2E tests
```

## 📊 Viewing Reports

This project uses Allure for reporting. After running the tests, an `allure-results` folder will be generated.

To view the report, run:
```bash
allure serve allure-results
```

## 💡 Highlighted Test Strategies

### The "Hybrid" Approach
In `tests/hybrid/test_hybrid_checkout.py`, the test doesn't log in via the UI. Instead, the `authenticated_context` fixture:
1. Registers a unique user via a `POST /users/register` request.
2. Authenticates the user via a `POST /users/login` request.
3. Retrieves the JWT token.
4. Opens a fresh Playwright Browser Context and injects the token into `window.localStorage['auth-token']`.
5. The UI test then immediately navigates to `/checkout`, completely bypassing the login screen.
