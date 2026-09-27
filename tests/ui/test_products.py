import pytest
from playwright.sync_api import expect
from utils.json_utils import load_json_data
from pages.products_page import ProductsPage
from pages.product_details_page import ProductDetailsPage

products_data = load_json_data("products_data.json")
sort_data = load_json_data("sort_data.json")

# Multi-line form for applying several marks to every test in this module:
# pytestmark = [
#     pytest.mark.ui,
#     pytest.mark.auth,
#     pytest.mark.regression,
# ]
pytestmark = [pytest.mark.ui, pytest.mark.readonly]


@pytest.mark.smoke
def test_products_are_displayed(logged_in_page):
    """Inventory page shows the expected product catalog."""
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()

    expect(products_page.title).to_be_visible()
    assert products_page.get_product_count() == 6
    names = products_page.get_product_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Fleece Jacket" in names


@pytest.mark.regression
@pytest.mark.parametrize("product", products_data)
def test_verify_product_details(logged_in_page, product):
    """Product details page shows name, price, and description for each dataset."""
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()
    products_page.open_product_details(product["product_name"])

    details_page = ProductDetailsPage(logged_in_page)
    details_page.wait_until_loaded()

    assert details_page.get_name() == product["product_name"]
    assert details_page.get_price() == product["expected_price"]
    assert product["description_contains"].lower() in details_page.get_description().lower()


@pytest.mark.regression
@pytest.mark.parametrize("sort_case", sort_data)
def test_sort_products(logged_in_page, sort_case):
    """Product sort dropdown reorders inventory by name or price."""
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()
    products_page.sort_products(sort_case["sort_option"])

    names = products_page.get_product_names()
    prices = products_page.get_product_prices()
    sort_type = sort_case["sort_type"]

    if sort_type == "name_asc":
        assert names == sorted(names)
    elif sort_type == "name_desc":
        assert names == sorted(names, reverse=True)
    elif sort_type == "price_asc":
        assert prices == sorted(prices)
    elif sort_type == "price_desc":
        assert prices == sorted(prices, reverse=True)
    else:
        raise AssertionError(f"Unknown sort type: {sort_type}")
