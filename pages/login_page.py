from pages.base_page import BasePage
from utils.logger import log_data, log_step
from utils.logger import log_step

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        log_step(self.logger, "Initializing LoginPage")
        self.username = page.locator("#user-name")
        self.password = page.locator("#password")
        self.login_button = page.locator("#login-button")
        log_step(self.logger, "Login button locator initialized")

    def login(self, username, password):
        log_step(self.logger, "Logging in with username and password")
        log_data(self.logger, {"username": username})
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()
        log_step(self.logger, "Login button clicked")