from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get("http://uitestingplayground.com/ajax")

try:
    blue_button = driver.find_element(By.ID, "ajaxButton")
    blue_button.click()
    green_banner = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "p.bg-success"))
    )
    banner_text = green_banner.text
    print(banner_text)
    
except Exception as e:
    print(f"Произошла ошибка: {e}")
    
finally:
    driver.quit()
