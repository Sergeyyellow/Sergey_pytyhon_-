"""
Страница с товарами интернет-магазина.
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class InventoryPage(BasePage):
    """
    Класс для работы со страницей товаров.
    """

    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    BOLT_TSHIRT_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ONESIE_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-onesie")
    
    def add_backpack_to_cart(self) -> 'InventoryPage':
        """
        Добавляет рюкзак в корзину.
        
        Returns:
            InventoryPage - текущий объект страницы
        """
        add_button = self.driver.find_element(*self.BACKPACK_ADD_BUTTON)
        add_button.click()
        return self
    
    def add_bolt_tshirt_to_cart(self) -> 'InventoryPage':
        """
        Добавляет футболку Bolt в корзину.
        
        Returns:
            InventoryPage - текущий объект страницы
        """
        add_button = self.driver.find_element(*self.BOLT_TSHIRT_ADD_BUTTON)
        add_button.click()
        return self
    
    def add_onesie_to_cart(self) -> 'InventoryPage':
        """
        Добавляет комбинезон в корзину.
        
        Returns:
            InventoryPage - текущий объект страницы
        """
        add_button = self.driver.find_element(*self.ONESIE_ADD_BUTTON)
        add_button.click()
        return self
    
    def get_cart_items_count(self) -> int:
        """
        Возвращает количество товаров в корзине.
        
        Returns:
            int - количество товаров в корзине
        """
        try:
            cart_badge = self.driver.find_element(*self.CART_BADGE)
            return int(cart_badge.text)
        except:
            return 0
    
    def go_to_cart(self) -> None:
        """Переходит в корзину."""
        self.driver.get("https://www.saucedemo.com/cart.html")