from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_slow_calculator():
    driver = webdriver.Chrome()
    
    try:
        # Шаг 1: Открыть страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        
        # Шаг 2: Ввести задержку 45
        delay_input = driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys("45")
        
        # Шаг 3: Нажать кнопки 7 + 8 =
        driver.find_element(By.XPATH, "//span[text()='7']").click()
        driver.find_element(By.XPATH, "//span[text()='+']").click()
        driver.find_element(By.XPATH, "//span[text()='8']").click()
        driver.find_element(By.XPATH, "//span[text()='=']").click()
        
        # Шаг 4: Проверить результат через 45 секунд
        wait = WebDriverWait(driver, 46)
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "screen"), "15"))
        
        result = driver.find_element(By.CLASS_NAME, "screen").text
        assert result == "15", f"Ожидался результат 15, но получен {result}"
        
    finally:
        driver.quit()