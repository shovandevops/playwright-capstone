import pytest
from config.env import load_env
from playwright.sync_api import sync_playwright, Playwright, APIRequestContext
from utils.logger import get_logger, log_step, log_data
from config.env import EnvConfig
from api_clients.posts_client import PostsClient

# @pytest.fixture()
# def page():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         yield page
#         context.close()
#         browser.close()

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
            extra_http_headers={"Content-Type": "application/json"}
        )
    yield request_context
    request_context.dispose()
    log_step(logger, "API context disposed")

@pytest.fixture()
def posts_client(api_context: APIRequestContext) -> PostsClient:
    return PostsClient(api_context)