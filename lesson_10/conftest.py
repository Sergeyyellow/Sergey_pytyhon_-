"""
Конфигурация pytest для Allure отчетов.
"""
import pytest
import allure
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации WebDriver.
    
    Yields:
        WebDriver - экземпляр драйвера Chrome
    """
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Хук для создания скриншотов при падении тестов.
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            driver = item.funcargs['driver']
            allure.attach(
                driver.get_screenshot_as_png(),
                name="screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print(f"Не удалось сделать скриншот: {e}")