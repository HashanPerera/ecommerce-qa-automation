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


@pytest.mark.ui
def test_invalid_login(page):
    page.goto(BASE_URL)

    page.get_by_placeholder("Username").fill("invalid_user")
    page.get_by_placeholder("Password").fill("wrong_password")
    page.get_by_role("button", name="Login").click()

    expect(
        page.locator('[data-test="error"]')
    ).to_contain_text("Username and password do not match")