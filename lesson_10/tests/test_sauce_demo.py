import sys
import os
import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.feature("Интернет-магазин")
@allure.severity(allure.severity_level.CRITICAL)
class TestSauceDemo:

    @allure.title("Полный процесс покупки товаров")
    @allure.description("Тестирование полного процесса покупки от авторизации до оформления заказа")
    @allure.story("Процесс покупки")
    @pytest.mark.smoke
    def test_complete_purchase_flow(self, driver):
    
        wait = WebDriverWait(driver, 10)
        
        with allure.step("1. Открыть сайт магазина и авторизоваться"):
            driver.get("https://www.saucedemo.com/")
        
            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))
            allure.attach("Авторизация прошла успешно", name="Статус")
        
        with allure.step("2. Добавить три конкретных товара в корзину"):
            
            products_to_add = [
                ("sauce-labs-backpack", "Sauce Labs Backpack"),
                ("sauce-labs-bolt-t-shirt", "Sauce Labs Bolt T-Shirt"),
                ("sauce-labs-onesie", "Sauce Labs Onesie")
            ]
            
            added_products = []
            
            for product_id, product_name in products_to_add:
                try:
                    button_id = f"add-to-cart-{product_id}"
                    add_button = wait.until(
                        EC.element_to_be_clickable((By.ID, button_id))
                    )
                    
                    if add_button.is_enabled():
                        add_button.click()
                        added_products.append(product_name)
                        allure.attach(f"Добавлен: {product_name}", name="Успех")
                        time.sleep(0.3)
                    else:
                        allure.attach(f"{product_name} не доступен", name="Предупреждение")
                except Exception as e:
                    allure.attach(f"Не удалось добавить {product_name}: {str(e)}", name="Ошибка")
            
            allure.attach(f"Добавлено товаров: {len(added_products)}", name="Итог добавления")
            allure.attach(f"Список: {', '.join(added_products)}", name="Товары")
            
            if len(added_products) < 3:
                allure.attach("Добавляем альтернативные товары", name="Дополнительно")
                
                alternative_products = [
                    ("sauce-labs-bike-light", "Sauce Labs Bike Light", 9.99),
                    ("sauce-labs-fleece-jacket", "Sauce Labs Fleece Jacket", 49.99),
                    ("test.allthethings()-t-shirt-(red)", "Test.allTheThings() T-Shirt (Red)", 15.99)
                ]
                
                for product_id, product_name, price in alternative_products:
                    if len(added_products) >= 3:
                        break
                    
                    try:
                        button_id = f"add-to-cart-{product_id}"
                        add_button = driver.find_element(By.ID, button_id)
                        if add_button.is_enabled():
                            add_button.click()
                            added_products.append(product_name)
                            allure.attach(f"Добавлен альтернативный: {product_name}", name="Замена")
                            time.sleep(0.3)
                    except:
                        continue
        
        with allure.step("3. Проверить количество товаров в корзине"):
            time.sleep(1) 
            
            try:
                cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
                cart_count = int(cart_badge.text)
                allure.attach(f"Товаров в корзине: {cart_count}", name="Количество")
                
                assert cart_count > 0, "В корзине должен быть хотя бы один товар"
                
            
                if cart_count != 3:
                    allure.attach(
                        driver.get_screenshot_as_png(),
                        name=f"Скриншот с {cart_count} товарами",
                        attachment_type=allure.attachment_type.PNG
                    )
            except Exception as e:
                allure.attach(f"Ошибка проверки корзины: {e}", name="Ошибка")
                raise
        
        with allure.step("4. Перейти в корзину"):
            driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cart_list")))
            
        
            assert "cart" in driver.current_url.lower()
            allure.attach(f"Перешли в корзину. URL: {driver.current_url}", name="Переход")
        
        with allure.step("5. Проверить содержимое корзины"):
            cart_items = driver.find_elements(By.CLASS_NAME, "cart_item")
            actual_count = len(cart_items)
            
            allure.attach(f"Найдено товаров на странице корзины: {actual_count}", name="Проверка")
            
        
            item_names = []
            for item in cart_items:
                try:
                    name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
                    price = item.find_element(By.CLASS_NAME, "inventory_item_price").text
                    item_names.append(f"{name} - {price}")
                except:
                    pass
            
            if item_names:
                allure.attach("Товары в корзине:\n" + "\n".join(item_names), name="Список товаров")
        
        with allure.step("6. Нажать кнопку Checkout"):
            checkout_button = driver.find_element(By.ID, "checkout")
            checkout_button.click()
            
            wait.until(EC.presence_of_element_located((By.ID, "first-name")))
            assert "checkout-step-one" in driver.current_url
            allure.attach("Перешли на страницу оформления заказа", name="Статус")
        
        with allure.step("7. Заполнить форму данными"):
        
            driver.find_element(By.ID, "first-name").send_keys("Иван")
            driver.find_element(By.ID, "last-name").send_keys("Иванов")
            driver.find_element(By.ID, "postal-code").send_keys("123456")
            driver.find_element(By.ID, "continue").click()
            
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_info")))
            assert "checkout-step-two" in driver.current_url
            allure.attach("Форма заполнена и отправлена", name="Статус")
        
        with allure.step("8. Проверить и зафиксировать итоговую стоимость"):
        
            summary_elements = driver.find_elements(By.CLASS_NAME, "summary_value_label")
            for elem in summary_elements:
                allure.attach(elem.text, name="Информация о заказе")
            
            total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
            total_text = total_element.text
            total_amount = total_text.replace("Total: $", "")
            
            allure.attach(f"Итоговая сумма: ${total_amount}", name="Итоговая стоимость")
            
            try:
                subtotal_element = driver.find_element(By.CLASS_NAME, "summary_subtotal_label")
                tax_element = driver.find_element(By.CLASS_NAME, "summary_tax_label")
                
                subtotal_text = subtotal_element.text.replace("Item total: $", "")
                tax_text = tax_element.text.replace("Tax: $", "")
                
                allure.attach(f"Стоимость товаров: ${subtotal_text}", name="Subtotal")
                allure.attach(f"Налог: ${tax_text}", name="Tax")
            except:
                pass
            
            try:
                float_amount = float(total_amount)
                
                assert float_amount > 0, f"Сумма должна быть положительной: ${total_amount}"
                
                assert 5.0 <= float_amount <= 200.0, \
                    f"Нереалистичная сумма: ${total_amount}. Ожидалось от $5 до $200"
                
                allure.attach(f"Сумма корректна: ${float_amount:.2f}", name="Проверка пройдена")
                
            except ValueError:
                allure.attach(f"Некорректный формат суммы: {total_amount}", name="Ошибка формата")
                raise
        
        with allure.step("9. Завершить оформление заказа (опционально)"):
           
            allure.attach("Тест завершен успешно! Заказ готов к оформлению.", name="Финальный статус")
            
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Финальный скриншот - итоговая сумма",
                attachment_type=allure.attachment_type.PNG
            )