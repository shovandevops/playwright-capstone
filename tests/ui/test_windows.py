import pytest
from playwright.sync_api import expect
from pages.windows_page import WindowsPage

# Multi-line form for applying several marks to every test in this module:
# pytestmark = [
#     pytest.mark.ui,
#     pytest.mark.auth,
#     pytest.mark.regression,
# ]
pytestmark = [pytest.mark.ui, pytest.mark.readonly]


@pytest.mark.regression
def test_open_new_window_and_validate_child_page(page, env):
    """Opens a child tab via expect_page() and validates parent and child pages."""
    windows_page = WindowsPage(page)
    windows_page.open(env.the_internet_url)
    parent_url = f"{env.the_internet_url.rstrip('/')}/windows"

    assert len(page.context.pages) == 1

    child_page = windows_page.open_new_window()
    child_page.wait_for_url("**/windows/new")

    assert len(page.context.pages) == 2

    assert page.url == parent_url
    expect(windows_page.heading).to_be_visible()

    assert child_page.url == f"{parent_url}/new"
    expect(child_page).to_have_title("New Window")
    expect(child_page.get_by_role("heading", name="New Window")).to_be_visible()

    child_page.close()
    assert len(page.context.pages) == 1
    assert page.url == parent_url
