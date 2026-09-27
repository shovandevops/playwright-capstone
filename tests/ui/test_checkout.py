import pytest
from playwright.sync_api import expect
from utils.json_utils import load_json_data
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

checkout_data = load_json_data("checkout_data.json")

# Multi-line form for applying several marks to every test in this module:
# pytestmark = [
#     pytest.mark.ui,
#     pytest.mark.auth,
#     pytest.mark.regression,
# ]
pytestmark = [pytest.mark.ui]


@pytest.mark.smoke
@pytest.mark.regression
@pytest.mark.parametrize("order", checkout_data)
def test_complete_checkout_and_validate_order(logged_in_page, order):
    """End-to-end checkout succeeds for each JSON checkout dataset."""
    products_page = ProductsPage(logged_in_page)
    products_page.wait_until_loaded()
    products_page.add_product_to_cart(order["product_name"])
    products_page.open_cart()

    cart_page = CartPage(logged_in_page)
    cart_page.wait_until_loaded()
    assert order["product_name"] in cart_page.get_item_names()
    cart_page.proceed_to_checkout()

    checkout_page = CheckoutPage(logged_in_page)
    checkout_page.complete_checkout(
        order["first_name"],
        order["last_name"],
        order["postal_code"],
    )

    expect(checkout_page.complete_header).to_be_visible()
    expect(checkout_page.complete_text).to_be_visible()
