import sys
import os
import pytest
from selenium import webdriver
import time

# Добавляем родительскую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestSauceDemo:
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
        # Инициализация страниц
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
    
    def teardown_method(self):
        """Завершение после каждого теста"""
        self.driver.quit()
    
    def test_complete_purchase_flow(self):
        """Тест полного процесса покупки"""
        # 1. Открыть сайт магазина
        self.login_page.open()
        print("Сайт открыт")
        
        # 2. Авторизоваться как пользователь standard_user
        self.login_page.login("standard_user", "secret_sauce")
        print("Авторизация выполнена")
        
        # Проверить, что авторизация прошла успешно
        assert "inventory" in self.driver.current_url
        print("Успешно перешли на страницу товаров")
        
        # 3. Добавить товары в корзину
        self.inventory_page\
            .add_backpack_to_cart()\
            .add_bolt_tshirt_to_cart()\
            .add_onesie_to_cart()
        print("Товары добавлены в корзину")
        
        # Проверить, что в корзине 3 товара
        cart_count = self.inventory_page.get_cart_items_count()
        assert cart_count == 3, f"Ожидалось 3 товара в корзине, но найдено {cart_count}"
        print(f"В корзине {cart_count} товаров")
        
        # 4. Перейти в корзину
        self.inventory_page.go_to_cart()
        print("Перешли в корзину")
        
        # Проверить, что перешли на страницу корзины
        assert "cart" in self.driver.current_url
        print(f"Текущий URL: {self.driver.current_url}")
        
        # Проверить содержимое корзины
        cart_items = self.cart_page.get_cart_items_count()
        assert cart_items == 3, f"Ожидалось 3 товара в корзине, но найдено {cart_items}"
        print(f"В корзине подтверждено {cart_items} товаров")
        
        # 5. Нажать кнопку Checkout
        self.cart_page.click_checkout()
        print("Нажата кнопка Checkout")
        
        # Даем время для перехода
        time.sleep(2)
        
        # Проверить, что перешли на страницу оформления заказа
        current_url = self.driver.current_url
        print(f"Текущий URL после Checkout: {current_url}")
        assert "checkout-step-one" in current_url, f"Ожидался checkout-step-one в URL, но получен: {current_url}"
        print("Успешно перешли на страницу оформления заказа")
        
        # 6. Заполнить форму данными
        self.checkout_page\
            .fill_checkout_form("Ivan", "Ivanov", "123456")\
            .click_continue()
        print("Форма заполнена и отправлена")
        
        # Даем время для перехода
        time.sleep(2)
        
        # Проверить, что перешли на страницу подтверждения
        current_url = self.driver.current_url
        print(f"Текущий URL после Continue: {current_url}")
        assert "checkout-step-two" in current_url, f"Ожидался checkout-step-two в URL, но получен: {current_url}"
        print("Успешно перешли на страницу подтверждения заказа")
        
        # 7. Прочитать итоговую стоимость
        total_amount = self.checkout_page.get_total_amount()
        print(f"Итоговая сумма: ${total_amount}")
        
        # 8. Проверить, что итоговая сумма равна $58.29
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получена ${total_amount}"
        
        print("Тест завершен успешно! Итоговая сумма корректна.")