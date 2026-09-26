from playwright.sync_api import Locator, expect
from pages.base_page import BasePage
from utils.logger import log_data, log_step


class ProductsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        log_step(self.logger, "Initializing ProductsPage")
        self.title = page.get_by_text("Products", exact=True)
        self.inventory_items = page.locator(".inventory_item")
        self.inventory_names = page.locator(".inventory_item_name")
        self.inventory_prices = page.locator(".inventory_item_price")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.cart_link = page.locator(".shopping_cart_link")
        self.cart_badge = page.locator(".shopping_cart_badge")

    def wait_until_loaded(self):
        """Waits for inventory page URL and product list visibility."""
        self.page.wait_for_url("**/inventory.html")
        self.page.wait_for_load_state("domcontentloaded")
        self.title.wait_for(state="visible")
        self.inventory_items.first.wait_for(state="visible")

    def get_product_count(self) -> int:
        """Returns the number of visible product cards."""
        return self.inventory_items.count()

    def get_product_names(self) -> list[str]:
        """Returns all product names currently displayed."""
        return self.inventory_names.all_inner_texts()

    def get_product_prices(self) -> list[float]:
        """Returns product prices as floats (strips the $ prefix)."""
        raw_prices = self.inventory_prices.all_inner_texts()
        return [float(price.replace("$", "")) for price in raw_prices]

    def product_card(self, product_name: str) -> Locator:
        """Returns the inventory card locator for a product by name."""
        return self.inventory_items.filter(
            has=self.page.get_by_text(product_name, exact=True)
        )

    def add_product_to_cart(self, product_name: str):
        """Adds a product to the cart by clicking Add to cart on its card."""
        log_step(self.logger, f"Adding product to cart: {product_name}")
        card = self.product_card(product_name)
        card.wait_for(state="visible")
        card.get_by_role("button", name="Add to cart").click()
        log_data(self.logger, {"product": product_name, "action": "add"})

    def remove_product_from_cart(self, product_name: str):
        """Removes a product from the cart via the inventory Remove button."""
        log_step(self.logger, f"Removing product from cart: {product_name}")
        card = self.product_card(product_name)
        card.wait_for(state="visible")
        card.get_by_role("button", name="Remove").click()
        log_data(self.logger, {"product": product_name, "action": "remove"})

    def open_product_details(self, product_name: str):
        """Navigates to the product details page by clicking the product name."""
        log_step(self.logger, f"Opening product details: {product_name}")
        self.page.get_by_text(product_name, exact=True).click()
        self.page.wait_for_url("**/inventory-item.html**")
        self.page.wait_for_load_state("domcontentloaded")

    def get_cart_count(self) -> int:
        """Returns the cart badge count, or 0 when the badge is absent."""
        if self.cart_badge.count() == 0:
            return 0
        return int(self.cart_badge.inner_text())

    def open_cart(self):
        """Opens the shopping cart page."""
        log_step(self.logger, "Opening shopping cart")
        self.cart_link.click()
        self.page.wait_for_url("**/cart.html")
        self.page.wait_for_load_state("domcontentloaded")

    def sort_products(self, option_label: str):
        """Sorts products using the product sort dropdown label."""
        log_step(self.logger, f"Sorting products by: {option_label}")
        self.sort_dropdown.wait_for(state="visible")
        self.sort_dropdown.select_option(label=option_label)
        expect(self.inventory_items.first).to_be_visible()
