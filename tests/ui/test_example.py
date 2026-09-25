import re
from playwright.sync_api import Page, expect
import pytest
from config.settings import EnvConfig
from pages.base_page import BasePage
from utils.logger import log_step, log_data


def test_has_title(page, env: EnvConfig):
    base_page = BasePage(page)
    log_step(base_page.logger, "Starting test_has_title")
    base_page.goto(env.saucedemo_url)

    # Expect a title "to contain" a substring.
    expect(base_page.page).to_have_title(re.compile("Swag Labs"))
    log_step(base_page.logger, "Test_has_title completed")

def test_get_started_link(page, env: EnvConfig):
    base_page = BasePage(page)
    log_step(base_page.logger, "Starting test_get_started_link")
    base_page.goto(env.demoqa_url)

    # Click the get started link.
  
    with base_page.page.context.expect_page() as new_page_info:
        base_page.page.get_by_alt_text("Selenium Online Training").click()
    new_page = new_page_info.value
    new_page.wait_for_load_state("domcontentloaded")

    assert new_page.url == "https://www.toolsqa.com/selenium-training/"

    # Expects page to have a heading with the name of Installation.
    expect(new_page.get_by_text("Go To Registration")).to_be_visible()
    log_step(base_page.logger, "Test_get_started_link completed")