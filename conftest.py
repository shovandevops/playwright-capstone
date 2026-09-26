import pytest
from playwright.sync_api import Playwright, APIRequestContext, Page
from config.env import load_env
from config.settings import EnvConfig
from api_clients.posts_client import PostsClient
from api_clients.users_client import UsersClient
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.logger import get_logger, log_step
from utils import session_storage
from utils.json_utils import load_json_data


@pytest.fixture(scope="session")
def env():
    return load_env()


@pytest.fixture(autouse=True)
def test_logger(request):
    logger = get_logger(request.node.name)
    log_step(logger, f"Starting test: {request.node.name}")
    yield
    log_step(logger, f"Completed test: {request.node.name}")


def pytest_html_report_title(report):
    report.title = "Playwright E2E Automation Report"


@pytest.fixture(scope="session")
def api_base_url(env: EnvConfig) -> str:
    return env.jsonplaceholder_url


@pytest.fixture()
def api_context(playwright: Playwright, api_base_url: str) -> APIRequestContext:
    logger = get_logger("api_context")
    log_step(logger, f"Creating API context for {api_base_url}")
    request_context = playwright.request.new_context(
        base_url=api_base_url,
        extra_http_headers={"Content-Type": "application/json"},
    )
    yield request_context
    request_context.dispose()
    log_step(logger, "API context disposed")


@pytest.fixture()
def posts_client(api_context: APIRequestContext) -> PostsClient:
    return PostsClient(api_context)


@pytest.fixture()
def users_client(api_context: APIRequestContext) -> UsersClient:
    return UsersClient(api_context)


@pytest.fixture()
def logged_in_page(page: Page, env: EnvConfig):
    """
    Logs in as standard_user, yields the authenticated page, then clears
    sessionStorage on teardown so cart state does not leak between tests.
    """
    credentials = next(
        item
        for item in load_json_data("login_data.json")
        if item["username"] == "standard_user"
    )
    login_page = LoginPage(page)
    login_page.goto(env.saucedemo_url)
    page.wait_for_load_state("domcontentloaded")
    login_page.login(credentials["username"], credentials["password"])
    products_page = ProductsPage(page)
    products_page.wait_until_loaded()
    yield page
    # SauceDemo cart lives in localStorage; assignment helpers use sessionStorage
    session_storage.clear_session_storage(page)
    page.evaluate("() => localStorage.clear()")