from pages.base_page import BasePage
from utils.logger import log_data, log_step


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        log_step(self.logger, "Initializing LoginPage")
        self.username = page.get_by_placeholder("Username")
        self.password = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_message = page.locator(".error-message-container")

    def login(self, username: str, password: str):
        """Fills credentials and submits the login form."""
        log_step(self.logger, "Logging in with username and password")
        log_data(self.logger, {"username": username})
        self.username.wait_for(state="visible")
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        log_step(self.logger, "Login button clicked")

    def get_error_text(self) -> str:
        """Returns the visible login error message text."""
        self.error_message.wait_for(state="visible")
        return self.error_message.inner_text()
