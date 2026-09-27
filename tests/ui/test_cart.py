import pytest
from utils.json_utils import load_json_data
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

cart_data = load_json_data("cart_data.json")

# Multi-line form for applying several marks to every test in this module:
# pytestmark = [
#     pytest.mark.ui,
#     pytest.mark.auth,
#     pytest.mark.regression,
# ]
pytestmark = [pytest.mark.ui]


@pytest.mark.smoke
def test_add_product_to_cart_and_validate_count(logged_in_page):
    """Adding a product increments the cart badge count."""
    product_name = cart_data["product_name"]
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()

    assert products_page.get_cart_count() == 0
    products_page.add_product_to_cart(product_name)
    products_page.cart_badge.wait_for(state="visible")
    assert products_page.get_cart_count() == 1


@pytest.mark.regression
def test_remove_product_from_cart(logged_in_page):
    """Removing a product from inventory clears the cart badge."""
    product_name = cart_data["product_name"]
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()

    products_page.add_product_to_cart(product_name)
    assert products_page.get_cart_count() == 1

    products_page.remove_product_from_cart(product_name)
    assert products_page.get_cart_count() == 0


@pytest.mark.regression
def test_remove_product_from_cart_page(logged_in_page):
    """Removing a line item from the cart page empties the cart."""
    product_name = cart_data["product_name"]
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()
    products_page.add_product_to_cart(product_name)
    products_page.open_cart()

    cart_page = CartPage(logged_in_page)
    cart_page.wait_until_loaded()
    assert product_name in cart_page.get_item_names()

    cart_page.remove_item(product_name)
    assert cart_page.get_item_count() == 0
