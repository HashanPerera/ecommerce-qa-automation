import pytest


BASE_URL = "https://fakestoreapi.com"


@pytest.mark.api
def test_get_all_products_returns_a_list(api_session):
    response = api_session.get(
        f"{BASE_URL}/products",
        timeout=15,
    )

    assert response.status_code == 200

    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0


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


@pytest.mark.api
def test_product_response_contains_valid_rating(api_session):
    response = api_session.get(
        f"{BASE_URL}/products/1",
        timeout=15,
    )

    assert response.status_code == 200

    rating = response.json()["rating"]

    assert isinstance(rating["rate"], (int, float))
    assert 0 <= rating["rate"] <= 5
    assert isinstance(rating["count"], int)
    assert rating["count"] >= 0