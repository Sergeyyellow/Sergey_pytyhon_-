from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_click_dynamic_id_button():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("http://uitestingplayground.com/dynamicid")
        time.sleep(2)
        blue_button = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
        blue_button.click()
        print("✅ Клик по синей кнопке с динамическим ID выполнен успешно!")
        time.sleep(2)
        
    except Exception as e:
        print(f"❌ Произошла ошибка: {e}")
        
    finally:
        if 'driver' in locals():
            driver.quit()
        print("Браузер закрыт.")

if __name__ == "__main__":
    test_click_dynamic_id_button()