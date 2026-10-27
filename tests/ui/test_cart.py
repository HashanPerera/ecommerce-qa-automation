import pytest
from playwright.sync_api import expect


BASE_URL = "https://www.saucedemo.com/"


@pytest.mark.ui
def test_add_product_to_cart(page):
    page.goto(BASE_URL)

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    backpack = page.locator(
        '[data-test="add-to-cart-sauce-labs-backpack"]'
    )
    backpack.click()

    expect(
        page.locator(".shopping_cart_badge")
    ).to_have_text("1")

    page.locator(".shopping_cart_link").click()

    expect(
        page.get_by_text(
            "Sauce Labs Backpack", exact=True
        )
    ).to_be_visible()