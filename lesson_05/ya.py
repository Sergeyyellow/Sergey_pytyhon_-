from time import sleep #импортировали метод из пакета
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(
service=ChromeService(ChromeDriverManager().install()))

driver.get("https://ya.ru/")
driver.get("https://vk.com/")
for x in range(1, 10):
	driver.back()
	driver.forward()
sleep(50) #установили «засыпание» браузера на 50 секунд