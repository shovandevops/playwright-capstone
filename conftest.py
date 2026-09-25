import pytest
from config.env import load_env
from playwright.sync_api import sync_playwright
from utils.logger import get_logger, log_step, log_data

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