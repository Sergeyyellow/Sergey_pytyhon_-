from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_shopping_cart_total():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Шаг 1: Открыть сайт
        driver.get("https://www.saucedemo.com/")
        
        # Шаг 2: Авторизоваться
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Ожидаем загрузки
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
        
        # Шаг 3: Добавить товары в корзину
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-bolt-t-shirt").click()
        driver.find_element(By.ID, "add-to-cart-sauce-labs-onesie").click()
        
        # Шаг 4: Перейти в корзину
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        
        # Шаг 5: Нажать Checkout
        wait.until(EC.presence_of_element_located((By.ID, "checkout")))
        driver.find_element(By.ID, "checkout").click()
        
        # Шаг 6: Заполнить форму
        wait.until(EC.presence_of_element_located((By.ID, "first-name")))
        driver.find_element(By.ID, "first-name").send_keys("Иван")
        driver.find_element(By.ID, "last-name").send_keys("Петров")
        driver.find_element(By.ID, "postal-code").send_keys("123456")
        
        # Шаг 7: Нажать Continue
        driver.find_element(By.ID, "continue").click()
        
        # Шаг 8: Прочитать итоговую стоимость
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
        total_element = driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text
        total_amount = total_text.replace("Total: $", "")
        
        # Шаг 9: Проверить сумму
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получена ${total_amount}"
        
    finally:
        driver.quit()