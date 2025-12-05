from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class InventoryPage(BasePage):
    # Локаторы
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    # Товары
    BACKPACK_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-backpack")
    BOLT_TSHIRT_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ONESIE_ADD_BUTTON = (By.ID, "add-to-cart-sauce-labs-onesie")
    
    def add_backpack_to_cart(self):
        """Добавляет рюкзак в корзину"""
        add_button = self.driver.find_element(*self.BACKPACK_ADD_BUTTON)
        add_button.click()
        return self
    
    def add_bolt_tshirt_to_cart(self):
        """Добавляет футболку Bolt в корзину"""
        add_button = self.driver.find_element(*self.BOLT_TSHIRT_ADD_BUTTON)
        add_button.click()
        return self
    
    def add_onesie_to_cart(self):
        """Добавляет комбинезон в корзину"""
        add_button = self.driver.find_element(*self.ONESIE_ADD_BUTTON)
        add_button.click()
        return self
    
    def get_cart_items_count(self):
        """Возвращает количество товаров в корзине"""
        try:
            cart_badge = self.driver.find_element(*self.CART_BADGE)
            return int(cart_badge.text)
        except:
            return 0
    
    def go_to_cart(self):
        """Переходит в корзину"""
        print("Попытка перейти в корзину...")
        
        # Попробуем разные локаторы для корзины
        cart_selectors = [
            (By.CLASS_NAME, "shopping_cart_link"),
            (By.CSS_SELECTOR, ".shopping_cart_link"),
            (By.CSS_SELECTOR, "a.shopping_cart_link"),
            (By.CSS_SELECTOR, "[data-test='shopping-cart-link']"),
            (By.XPATH, "//a[contains(@class, 'shopping_cart_link')]"),
            (By.XPATH, "//div[@class='shopping_cart_container']/a")
        ]
        
        for selector in cart_selectors:
            try:
                print(f"Пробуем локатор корзины: {selector}")
                cart_link = self.wait.until(
                    EC.element_to_be_clickable(selector)
                )
                print(f"Ссылка корзины найдена: {cart_link.get_attribute('outerHTML')}")
                cart_link.click()
                print("Клик по корзине выполнен")
                
                # Ждем перехода на страницу корзины
                self.wait.until(EC.url_contains("cart"))
                print("Успешно перешли на страницу корзины")
                return
            except Exception as e:
                print(f"Локатор {selector} не сработал: {e}")
                continue
        
        raise Exception("Не удалось найти и нажать ссылку корзины")