from pages.base_page import BasePage
from utils.logger import log_step


class ProductDetailsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        log_step(self.logger, "Initializing ProductDetailsPage")
        self.product_name = page.locator(".inventory_details_name")
        self.product_description = page.locator(".inventory_details_desc")
        self.product_price = page.locator(".inventory_details_price")
        self.add_to_cart = page.get_by_role("button", name="Add to cart")
        self.back_to_products = page.get_by_role("button", name="Back to products")

    def wait_until_loaded(self):
        """Waits for product details content to be visible."""
        self.page.wait_for_url("**/inventory-item.html**")
        self.page.wait_for_load_state("domcontentloaded")
        self.product_name.wait_for(state="visible")

    def get_name(self) -> str:
        """Returns the product name on the details page."""
        return self.product_name.inner_text()

    def get_description(self) -> str:
        """Returns the product description text."""
        return self.product_description.inner_text()

    def get_price(self) -> str:
        """Returns the product price text including currency symbol."""
        return self.product_price.inner_text()
