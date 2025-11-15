from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_form_validation():
    driver = webdriver.Edge()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Шаг 1: Открыть страницу
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/data-types.html")
        
        # Шаг 2: Заполнить форму
        driver.find_element(By.ID, "first-name").send_keys("Иван")
        driver.find_element(By.ID, "last-name").send_keys("Петров")
        driver.find_element(By.ID, "address").send_keys("Ленина, 55-3")
        driver.find_element(By.ID, "e-mail").send_keys("test@skypro.com")
        driver.find_element(By.ID, "phone").send_keys("+7985899998787")
        # Zip code оставляем пустым
        driver.find_element(By.ID, "city").send_keys("Москва")
        driver.find_element(By.ID, "country").send_keys("Россия")
        driver.find_element(By.ID, "job-position").send_keys("QA")
        driver.find_element(By.ID, "company").send_keys("SkyPro")
        
        # Шаг 3: Нажать кнопку Submit
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        # Ожидание применения стилей
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".is-invalid")))
        
        # Шаг 4: Проверить, что поле Zip code подсвечено красным
        zip_code_field = driver.find_element(By.ID, "zip-code")
        assert "is-invalid" in zip_code_field.get_attribute("class"), "Zip code должен быть красным"
        
        # Шаг 5: Проверить, что остальные поля подсвечены зеленым
        fields_to_check = ["first-name", "last-name", "address", "e-mail", "phone", "city", "country", "job-position", "company"]
        
        for field_id in fields_to_check:
            field = driver.find_element(By.ID, field_id)
            assert "is-valid" in field.get_attribute("class"), f"Поле {field_id} должно быть зеленым"
            
    finally:
        driver.quit()