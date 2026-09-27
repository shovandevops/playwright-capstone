from pages.base_page import BasePage
from utils.logger import log_data, log_step


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        log_step(self.logger, "Initializing CartPage")
        self.title = page.get_by_text("Your Cart", exact=True)
        self.cart_items = page.locator(".cart_item")
        self.cart_item_names = page.locator(".inventory_item_name")
        self.checkout_button = page.get_by_role("button", name="Checkout")
        self.continue_shopping = page.get_by_role("button", name="Continue Shopping")

    def wait_until_loaded(self):
        """Waits for cart page URL and title visibility."""
        self.page.wait_for_url("**/cart.html")
        self.page.wait_for_load_state("domcontentloaded")
        self.title.wait_for(state="visible")

    def get_item_names(self) -> list[str]:
        """Returns names of items currently in the cart."""
        return self.cart_item_names.all_inner_texts()

    def get_item_count(self) -> int:
        """Returns the number of cart line items."""
        return self.cart_items.count()

    def remove_item(self, product_name: str):
        """Removes a cart line item by product name."""
        log_step(self.logger, f"Removing cart item: {product_name}")
        item = self.cart_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )
        item.wait_for(state="visible")
        item.get_by_role("button", name="Remove").click()
        log_data(self.logger, {"product": product_name, "action": "remove_from_cart"})

    def proceed_to_checkout(self):
        """Clicks Checkout and waits for the information step."""
        log_step(self.logger, "Proceeding to checkout")
        self.checkout_button.click()
        self.page.wait_for_url("**/checkout-step-one.html")
        self.page.wait_for_load_state("domcontentloaded")
