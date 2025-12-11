from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import time

def test_input_operations():
    try:
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
        driver.get("http://the-internet.herokuapp.com/inputs")
        time.sleep(2)
        input_field = driver.find_element(By.TAG_NAME, "input")
        input_field.send_keys("Sky")
        print("✅ Текст 'Sky' введен в поле")
        time.sleep(1)
        input_field.clear()
        print("✅ Поле очищено")
        time.sleep(1)
        input_field.send_keys("Pro")
        print("✅ Текст 'Pro' введен в поле")
        time.sleep(1)
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        
    finally:
        if 'driver' in locals():
            driver.quit()
        print("✅ Браузер закрыт методом quit()")

if __name__ == "__main__":
    test_input_operations()