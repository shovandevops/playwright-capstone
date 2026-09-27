import pytest
from playwright.sync_api import expect
from utils.json_utils import load_json_data
from pages.login_page import LoginPage
from pages.products_page import ProductsPage

login_data = load_json_data("login_data.json")
valid_data = [d for d in login_data if d["username"] == "standard_user"]
locked_out_data = [d for d in login_data if d["username"] == "locked_out_user"]
invalid_data = [d for d in login_data if d["username"] == "invalid_user"]

# Multi-line form for applying several marks to every test in this module:
# pytestmark = [
#     pytest.mark.ui,
#     pytest.mark.auth,
#     pytest.mark.regression,
# ]
pytestmark = [pytest.mark.ui, pytest.mark.auth]


@pytest.mark.smoke
@pytest.mark.parametrize("credentials", valid_data)
def test_valid_login(page, env, credentials):
    """Valid login navigates successfully to the inventory page."""
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    page.wait_for_load_state("domcontentloaded")
    assert login_page.url == env.saucedemo_url

    login_page.login(credentials["username"], credentials["password"])
    products_page = ProductsPage(page)
    products_page.wait_until_loaded()
    expect(products_page.title).to_be_visible()


@pytest.mark.regression
@pytest.mark.parametrize("credentials", invalid_data)
def test_invalid_login(page, env, credentials):
    """Invalid credentials show the expected error message."""
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    page.wait_for_load_state("domcontentloaded")

    login_page.login(credentials["username"], credentials["password"])
    assert (
        login_page.get_error_text()
        == "Epic sadface: Username and password do not match any user in this service"
    )


@pytest.mark.regression
@pytest.mark.parametrize("credentials", locked_out_data)
def test_locked_out_user_login(page, env, credentials):
    """Locked-out user sees the locked-out error message."""
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    page.wait_for_load_state("domcontentloaded")

    login_page.login(credentials["username"], credentials["password"])
    assert (
        login_page.get_error_text()
        == "Epic sadface: Sorry, this user has been locked out."
    )
