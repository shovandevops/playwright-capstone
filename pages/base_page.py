from playwright.sync_api import Page
from utils.logger import get_logger, log_step, log_data
from typing import Optional
from playwright.sync_api import Response
from playwright.sync_api import Locator
class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def goto(self, url: str, **kwargs) -> Optional[Response]:
        """Navigates to the specified URL with logging."""
        log_step(self.logger, f"Navigating to URL: {url}")
        return self.page.goto(url, **kwargs)

    @property
    def url(self) -> str:
        """Returns the current page URL."""
        return self.page.url
    
    
    def locator(self, locator: str) -> Locator:
        """Returns a locator for the specified selector."""
        return self.page.locator(locator)
    
    