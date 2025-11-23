from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class CartPage(BasePage):
    # Локаторы
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "button[data-test='checkout']")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    
    def click_checkout(self):
        """Нажимает кнопку Checkout"""
        # Ждем появления кнопки
        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[data-test='checkout']"))
        )
        
        # Прокручиваем к кнопке чтобы она была видимой
        self.driver.execute_script("arguments[0].scrollIntoView(true);", checkout_button)
        
        # Ждем пока кнопка станет кликабельной
        checkout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='checkout']"))
        )
        
        # Нажимаем кнопку
        checkout_button.click()
        
        # Ждем перехода на следующую страницу
        WebDriverWait(self.driver, 10).until(
            EC.url_contains("checkout-step-one")
        )
    
    def get_cart_items_count(self):
        """Возвращает количество товаров в корзине"""
        return len(self.driver.find_elements(*self.CART_ITEMS))
    
    def get_item_names(self):
        """Возвращает список названий товаров в корзине"""
        items = self.driver.find_elements(*self.ITEM_NAME)
        return [item.text for item in items]