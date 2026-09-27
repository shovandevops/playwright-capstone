from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import log_data, log_step


class WindowsPage(BasePage):
    """Page object for the-internet 'Multiple Windows' page (/windows)."""

    PATH = "windows"

    def __init__(self, page: Page):
        super().__init__(page)
        log_step(self.logger, "Initializing WindowsPage")
        self.heading = page.get_by_role("heading", name="Opening a new window")
        self.click_here_link = page.get_by_role("link", name="Click Here")

    def open(self, base_url: str):
        """Navigates to the Multiple Windows page and waits for it to load."""
        self.goto(f"{base_url.rstrip('/')}/{self.PATH}")
        self.page.wait_for_load_state("domcontentloaded")
        self.heading.wait_for(state="visible")

    def open_new_window(self) -> Page:
        """Clicks 'Click Here' and returns the newly opened child page."""
        log_step(self.logger, "Opening new window via 'Click Here' link")
        with self.page.context.expect_page() as new_page_info:
            self.click_here_link.click()
        child_page = new_page_info.value
        child_page.wait_for_load_state("domcontentloaded")
        log_data(self.logger, {"child_url": child_page.url})
        return child_page
