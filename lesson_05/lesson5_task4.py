from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time

def test_login_and_get_message():
    try:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get("http://the-internet.herokuapp.com/login")
        time.sleep(2)
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys("tomsmith")
        print("✅ Логин 'tomsmith' введен")
        time.sleep(1)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("SuperSecretPassword!")
        print("✅ Пароль введен")
        time.sleep(1)
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        print("✅ Кнопка Login нажата")
        time.sleep(2)
        success_message = driver.find_element(By.ID, "flash")
        message_text = success_message.text
        print("✅ Текст с зеленой плашки:")
        print(f"📢 {message_text}")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        
    finally:
        if 'driver' in locals():
            driver.quit()
        print("✅ Браузер закрыт методом quit()")

if __name__ == "__main__":
    test_login_and_get_message()