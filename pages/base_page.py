from typing import Optional

from playwright.sync_api import Locator, Page, Response

from utils.logger import get_logger, log_debug, log_step, log_warning


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def goto(self, url: str, **kwargs) -> Optional[Response]:
        """Navigates to the specified URL, logging the response status."""
        log_step(self.logger, f"Navigating to URL: {url}")
        response = self.page.goto(url, **kwargs)
        if response is None:
            log_debug(self.logger, f"No response for {url} (same-document navigation)")
        elif not response.ok:
            log_warning(self.logger, f"Navigation to {url} returned HTTP {response.status}")
        else:
            log_debug(self.logger, f"Navigation to {url} returned HTTP {response.status}")
        return response

    @property
    def url(self) -> str:
        """Returns the current page URL."""
        return self.page.url

    def locator(self, locator: str) -> Locator:
        """Returns a locator for the specified selector."""
        return self.page.locator(locator)
