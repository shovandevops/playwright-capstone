class RegistrationPage:
    def __init__(self, page):
        self.page = page

        # Role-based locators
        self.submit_button = page.get_by_role("button", name="Register")
        self.cancel_link = page.get_by_role("link", name="Cancel")

        # Label-based locators
        self.first_name = page.get_by_label("First Name")
        self.last_name = page.get_by_label("Last Name")
        self.email = page.get_by_label("Email Address")

        # Placeholder-based locators
        self.password = page.get_by_placeholder("Enter password")
        self.confirm_password = page.get_by_placeholder("Confirm password")

    def register(self, data):
        self.first_name.fill(data["first_name"])
        self.last_name.fill(data["last_name"])
        self.email.fill(data["email"])
        self.password.fill(data["password"])
        self.confirm_password.fill(data["password"])
        self.submit_button.click()
