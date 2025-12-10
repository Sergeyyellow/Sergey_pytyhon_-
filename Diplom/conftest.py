import pytest
import allure
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Браузер для тестов: chrome или firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск в headless режиме"
    )
    parser.addoption(
        "--base-url",
        default="https://www.chitai-gorod.ru",
        help="Базовый URL для тестирования"
    )
    parser.addoption(
        "--retry-failed",
        action="store_true",
        default=False,
        help="Повторно запускать упавшие тесты"
    )


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base-url")
    
    driver = None
    
    try:
        if browser_name == "chrome":
            options = Options()
            if headless:
                options.add_argument("--headless=new")  # Новый headless режим
            
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-gpu")
            
            # Настраиваем user-agent и другие параметры для обхода защиты
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Добавляем дополнительные опции
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            
            # Используем webdriver-manager
            from selenium.webdriver.chrome.service import Service
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            
            # Настраиваем Firefox
            options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0")
            
            from selenium.webdriver.firefox.service import Service
            service = Service(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)
        
        else:
            pytest.skip(f"Браузер {browser_name} не поддерживается")
        
        # Настройки драйвера
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        # Сохраняем base_url в драйвере
        driver.base_url = base_url
        
        yield driver
        
    except Exception as e:
        # Пробуем альтернативный метод запуска
        try:
            if browser_name == "chrome":
                driver = webdriver.Chrome(options=Options())
                driver.base_url = base_url
                yield driver
            else:
                pytest.skip(f"Не удалось запустить браузер: {str(e)}")
        except:
            pytest.skip(f"Не удалось запустить браузер: {str(e)}")
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


# Добавляем поддержку повторного запуска упавших тестов
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания отчетов Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        item.test_result = rep
        
        # Если тест упал и включен retry, помечаем для перезапуска
        if rep.failed and item.config.getoption("--retry-failed"):
            item.add_marker(pytest.mark.flaky(reruns=1))
        
        # Делаем скриншот при падении UI тестов
        if rep.failed and "browser" in item.fixturenames:
            browser = item.funcargs.get("browser")
            if browser:
                try:
                    screenshot = browser.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name="screenshot_on_failure",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                    # Также сохраняем HTML страницы для отладки
                    page_source = browser.page_source[:5000]  # Первые 5000 символов
                    allure.attach(
                        page_source,
                        name="page_source_on_failure",
                        attachment_type=allure.attachment_type.TEXT
                    )
                except Exception as e:
                    allure.attach(
                        f"Не удалось сделать скриншот: {str(e)}",
                        name="screenshot_error",
                        attachment_type=allure.attachment_type.TEXT
                    )


def pytest_configure(config):
    """Регистрация пользовательских меток"""
    config.addinivalue_line("markers", "ui: UI тесты")
    config.addinivalue_line("markers", "api: API тесты")
    config.addinivalue_line("markers", "smoke: Smoke тесты")
    config.addinivalue_line("markers", "search: Тесты поиска")
    config.addinivalue_line("markers", "cart: Тесты корзины")
    config.addinivalue_line("markers", "auth: Тесты авторизации")
    config.addinivalue_line("markers", "flaky: Нестабильные тесты (перезапускаются)")