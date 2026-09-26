from pages.base_page import BasePage
from utils.logger import log_data, log_step


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        log_step(self.logger, "Initializing CheckoutPage")
        self.first_name = page.get_by_placeholder("First Name")
        self.last_name = page.get_by_placeholder("Last Name")
        self.postal_code = page.get_by_placeholder("Zip/Postal Code")
        self.continue_button = page.get_by_role("button", name="Continue")
        self.finish_button = page.get_by_role("button", name="Finish")
        self.complete_header = page.get_by_role("heading", name="Thank you for your order!")
        self.complete_text = page.get_by_text("Your order has been dispatched")

    def fill_customer_info(self, first_name: str, last_name: str, postal_code: str):
        """Fills checkout customer information fields."""
        log_step(self.logger, "Filling checkout customer information")
        log_data(
            self.logger,
            {
                "first_name": first_name,
                "last_name": last_name,
                "postal_code": postal_code,
            },
        )
        self.first_name.wait_for(state="visible")
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def continue_to_overview(self):
        """Continues from customer info to the order overview."""
        log_step(self.logger, "Continuing to checkout overview")
        self.continue_button.click()
        self.page.wait_for_url("**/checkout-step-two.html")
        self.page.wait_for_load_state("domcontentloaded")

    def finish_order(self):
        """Completes the order and waits for the confirmation page."""
        log_step(self.logger, "Finishing checkout order")
        self.finish_button.wait_for(state="visible")
        self.finish_button.click()
        self.page.wait_for_url("**/checkout-complete.html")
        self.page.wait_for_load_state("domcontentloaded")
        self.complete_header.wait_for(state="visible")

    def complete_checkout(self, first_name: str, last_name: str, postal_code: str):
        """Runs the full checkout flow through order confirmation."""
        self.fill_customer_info(first_name, last_name, postal_code)
        self.continue_to_overview()
        self.finish_order()
