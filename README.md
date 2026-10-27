E-commerce QA Automation Framework

A Python-based test automation portfolio project demonstrating UI testing, API validation, reusable test design, and continuous integration.

!Python !pytest !Playwright !API Testing !GitHub Actions

1. Project Overview

This project demonstrates how to design and implement an automated testing framework for e-commerce-related functionality using Python.

It combines browser-based testing with API testing to validate application behaviour, response data, and important user journeys. It also demonstrates the use of pytest fixtures, reusable test components, HTML reporting, and GitHub Actions.

The project uses two independent public demo services:

UI testing: SauceDemo — browser-based login and shopping basket scenarios.
API testing: Fake Store API — HTTP requests and product response validation.

These services are independent. The API tests do not validate the backend of SauceDemo, and the project does not claim end-to-end integration between the two services.

Project objectives
Automate positive and negative UI test scenarios.
Validate API status codes, response structures, data types, and business rules.
Apply reusable test fixtures and maintainable test organisation.
Generate HTML test reports.
Run tests automatically using GitHub Actions.
Demonstrate practical QA automation skills relevant to QA Automation Engineer and junior SDET roles.
2. Technology Stack
Technology	Purpose
Python	Programming language
pytest	Test execution, discovery, fixtures, and assertions
Playwright	Browser automation
pytest-playwright	Playwright integration with pytest
requests	HTTP API testing
pytest-html	HTML test reporting
Git	Version control
GitHub	Source code hosting
GitHub Actions	Continuous integration
3. Project Structure
ecommerce-qa-automation/
├── .github/
│   └── workflows/
│       └── tests.yml
├── pages/
│   └── login_page.py
├── tests/
│   ├── conftest.py
│   ├── ui/
│   │   ├── test_login.py
│   │   └── test_cart.py
│   └── api/
│       └── test_products.py
├── utils/
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md


Directory responsibilities

tests/ui/: Browser-based functional tests.
tests/api/: API response and data validation tests.
tests/conftest.py: Shared pytest fixtures, including the reusable HTTP session.
pages/: Page Object Model classes that encapsulate page locators and actions.
utils/: Reserved for shared utilities as the framework grows.
.github/workflows/: Automated test execution configuration.
pytest.ini: Test discovery and marker configuration.
requirements.txt: Python dependencies.
.gitignore: Excludes virtual environments, caches, reports, and generated test artifacts.

Some directories, such as utils/, are extension points and may remain empty in the initial version.

4. Prerequisites

Before running the project, install:

Python 3.11 or newer
Git
A GitHub account (required only for publishing the repository and using GitHub Actions)

An internet connection is required to access the public demo services and download browser dependencies.

5. Installation and Setup
Step 1: Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ecommerce-qa-automation


Replace the placeholder with your actual repository URL.

Step 2: Create a virtual environment
python -m venv .venv


Activate it on Windows PowerShell:

.venv\Scripts\Activate.ps1


On macOS or Linux:

source .venv/bin/activate

Step 3: Install dependencies

Install the required packages:

python -m pip install --upgrade pip
pip install pytest pytest-playwright playwright requests pytest-html


Install the Chromium browser:

python -m playwright install chromium

Step 4: Save the dependencies

After verifying that the environment works, record the installed versions:

pip freeze > requirements.txt


For reproducible installations, commit the verified requirements.txt file. Avoid regenerating it from an unrelated environment.

6. Automated Test Coverage
6.1 UI Testing with Playwright

The example UI suite covers the following scenarios.

Test scenario	Test objective
Valid login	Verify that valid credentials navigate to the inventory page
Invalid login	Verify that invalid credentials display an error
Add product to basket	Verify that the basket count increases
Basket contents	Verify that the selected product appears in the basket

The tests use Playwright's role-based and placeholder-based locators, as well as explicit assertions to verify user-visible behaviour.

Example test: Valid login

import pytest
from playwright.sync_api import expect


BASE_URL = "https://www.saucedemo.com/"


@pytest.mark.ui
def test_valid_login(page):
    page.goto(BASE_URL)

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(
        "https://www.saucedemo.com/inventory.html"
    )

    expect(
        page.get_by_text("Products", exact=True)
    ).to_be_visible()


The test checks the resulting application state rather than simply verifying that the login button can be clicked.

6.2 API Testing with requests

The API suite uses Fake Store API to demonstrate HTTP requests and response validation.

The example scenarios include:

Retrieving a product list.
Verifying the response status and data structure.
Checking required product fields.
Validating product prices and rating data.
Checking rating values against expected constraints.

Example test: Product response validation

import pytest


BASE_URL = "https://fakestoreapi.com"


@pytest.mark.api
def test_get_product_has_expected_fields(api_session):
    response = api_session.get(
        f"{BASE_URL}/products/1",
        timeout=15,
    )

    assert response.status_code == 200

    product = response.json()

    assert product["id"] == 1
    assert isinstance(product["title"], str)
    assert product["title"].strip() != ""
    assert isinstance(product["price"], (int, float))
    assert product["price"] >= 0
    assert isinstance(product["rating"], dict)


These checks validate the response's structure and selected data constraints. They do not constitute a complete API contract or security assessment.

6.3 Test Fixtures

The shared fixture in tests/conftest.py provides a reusable HTTP session:

import pytest
import requests


@pytest.fixture
def api_session():
    session = requests.Session()
    yield session
    session.close()


The fixture allows API tests to reuse a session and ensures it is closed after the test.

Playwright's pytest plugin provides the page fixture used by the browser tests.

7. Running the Tests

Run commands from the project root with the virtual environment activated.

Run the complete suite
pytest

Run only UI tests
pytest -m ui

Run only API tests
pytest -m api

Run UI tests in Chromium
pytest -m ui --browser chromium

Generate an HTML report

Create the reports directory first:

python -c "from pathlib import Path; Path('reports').mkdir(exist_ok=True)"


Run pytest with HTML reporting:

pytest --html=reports/report.html --self-contained-html


Open reports/report.html in a browser to inspect the generated report.

Test results depend on the current state and availability of the public demo services. No execution results are asserted in this documentation.

8. Continuous Integration with GitHub Actions

The workflow is configured in:

.github/workflows/tests.yml


The workflow is intended to:

Run when code is pushed or a pull request is opened.
Set up Python.
Install project dependencies.
Install Chromium and its required system dependencies.
Execute the automated tests.
Upload the HTML report and available browser evidence as workflow artifacts.

The workflow uses GitHub-hosted runners and accesses the same public demo services as the local test suite.

Viewing workflow results

After pushing the project to GitHub:

Open the repository.
Select the Actions tab.
Open a workflow run.
Review the job logs and test outcome.
Download the report artifacts if they were generated.

The workflow configuration is included in the repository, but successful execution should only be claimed after the workflow has actually completed successfully.

9. Reporting and Failure Investigation

HTML reporting is provided by pytest-html.

Playwright can also retain browser traces and screenshots when tests fail. These artefacts help investigate:

Incorrect locators
Unexpected application states
Timing-related issues
Navigation failures
Differences between local and CI environments

When a test fails, the recommended investigation process is:

Read the assertion and traceback.
Confirm that the application or API is available.
Inspect the response or browser state.
Determine whether the issue is in the application, the test, or the external service.
Fix the root cause and rerun the relevant test.

Generated reports and traces may contain page content or other sensitive information. Review them before publishing any artefacts.

10. Implemented Features vs Planned Improvements

The following distinction describes the initial example implementation. Update it as the repository evolves.

Implemented in the example code
Python-based pytest test suite.
Playwright browser testing for login and basket scenarios.
API testing using requests.
Validation of API status codes, response fields, data types, and rating constraints.
Shared HTTP session fixture.
Pytest UI and API markers.
Basic Page Object Model example for the login page.
GitHub Actions workflow configuration.
pytest-html reporting configuration.

The Page Object Model is demonstrated for the login page; the initial basket test still contains its own login steps. Refactoring all UI tests to use shared page objects remains an improvement.

Planned improvements
Expand the Page Object Model to inventory, basket, and checkout pages.
Add parametrised login tests and additional negative scenarios.
Add API tests for invalid IDs, missing fields, error handling, and other documented behaviours.
Add test-data management and configuration for different environments.
Add structured logging and improved failure diagnostics.
Add API schema validation against an explicit contract.
Add browser coverage beyond Chromium where appropriate.
Add linting, formatting, and type checking to the CI workflow.
Improve dependency pinning and supply-chain security.
Add coverage for checkout validation, sorting, filtering, and basket totals.
Publish selected, sanitised test reports and workflow badges after successful runs.

These items should be marked as complete only after implementation and verification.

11. Design Principles

The framework follows these principles:

Readability: Test names should describe the expected behaviour.
Maintainability: Repeated setup and page interactions should be reusable.
Reliability: Prefer explicit assertions and stable locators over arbitrary sleeps.
Isolation: Tests should avoid depending on execution order or shared mutable state.
Meaningful assertions: Verify expected behaviour rather than only checking that requests or clicks completed.
Honest reporting: Document actual test coverage and results without overstating them.
12. Limitations

This is a portfolio project using public demo services, not a production-grade testing platform.

External services may be unavailable, rate-limited, or changed without notice.
The UI and API tests exercise different applications.
Public demo data does not represent a complete commercial e-commerce system.
The initial suite does not provide comprehensive checkout, payment, performance, accessibility, or security coverage.
Passing tests demonstrate only the scenarios and assertions that were executed.

For a production environment, additional controls would be required for test data, credentials, environment isolation, service contracts, and release gates.

13. Skills Demonstrated

This project is intended to demonstrate practical experience with:

Python programming and test automation
pytest fixtures, markers, assertions, and test discovery
Playwright browser automation
HTTP API testing and JSON validation
Reusable test architecture and Page Object Model concepts
HTML reporting and failure investigation
Git version control and GitHub collaboration
Continuous integration using GitHub Actions
QA test design, positive and negative scenarios, and defect analysis
14. Author

Name: <YOUR NAME>

GitHub: <YOUR GITHUB PROFILE URL>

LinkedIn: <YOUR LINKEDIN PROFILE URL>

This project is part of my professional development in software quality assurance, test automation, and Python-based testing.

Note: Replace the author placeholders, verify all installation instructions against the committed files, and update the implemented-features section as the project develops. Add actual test counts, screenshots, and workflow badges only after generating and verifying them.