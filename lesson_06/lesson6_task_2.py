from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome()
driver.get("http://uitestingplayground.com/textinput")

try:
    text_input = driver.find_element(By.ID, "newButtonName")
    text_input.clear()
    text_input.send_keys("SkyPro")
    blue_button = driver.find_element(By.ID, "updatingButton")
    blue_button.click()
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element((By.ID, "updatingButton"), "SkyPro")
    )
    button_text = blue_button.text
    print(button_text)
    
finally:
    driver.quit()
