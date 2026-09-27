import pytest
from pages.products_page import ProductsPage
from utils import session_storage
from utils.json_utils import load_json_data

cart_data = load_json_data("cart_data.json")

# Multi-line form for applying several marks to every test in this module:
# pytestmark = [
#     pytest.mark.ui,
#     pytest.mark.auth,
#     pytest.mark.regression,
# ]
pytestmark = [pytest.mark.ui]


@pytest.mark.regression
def test_session_storage_cart_lifecycle(logged_in_page):
    """
    Demonstrates write/read/save/clear/restore/validate for sessionStorage.

    Why page.context.cookies() does not capture sessionStorage:
    cookies are HTTP cookie-jar state; sessionStorage is a separate per-tab
    Web Storage API. Playwright's context.cookies() only returns cookies.

    Note: SauceDemo currently persists cart IDs in localStorage ('cart-contents').
    This test writes equivalent values into sessionStorage to satisfy the
    assignment's sessionStorage helper requirements.
    """
    page = logged_in_page
    products_page = ProductsPage(page)
    products_page.wait_until_loaded()
    products_page.add_product_to_cart(cart_data["product_name"])
    products_page.cart_badge.wait_for(state="visible")

    # Mirror cart state into sessionStorage for the assignment workflow
    local_cart = page.evaluate("() => localStorage.getItem('cart-contents')")
    session_storage.write_session_item(page, "cart-contents", local_cart or "[]")
    session_storage.write_session_item(page, "last_product", cart_data["product_name"])

    # Cookies never contain sessionStorage entries
    cookies = page.context.cookies()
    cookie_names = {cookie["name"] for cookie in cookies}
    assert "cart-contents" not in cookie_names
    assert "last_product" not in cookie_names

    cart_contents = session_storage.read_session_item(page, "cart-contents")
    assert cart_contents is not None
    assert cart_contents != "[]"
    assert session_storage.read_session_item(page, "last_product") == cart_data["product_name"]

    saved = session_storage.save_session_storage(page)
    assert saved["cart-contents"] == cart_contents
    assert saved["last_product"] == cart_data["product_name"]

    session_storage.clear_session_storage(page)
    assert session_storage.read_session_item(page, "cart-contents") is None
    assert session_storage.read_all_session_storage(page) == {}

    restored = session_storage.restore_session_storage(page)
    assert restored["cart-contents"] == saved["cart-contents"]
    assert restored["last_product"] == saved["last_product"]
    assert session_storage.validate_session_storage(page, saved)
