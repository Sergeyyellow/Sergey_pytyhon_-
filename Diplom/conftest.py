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
    """Добавление пользовательских опций командной строки"""
    
    # Группа для Selenium/UI тестов
    selenium_group = parser.getgroup("selenium", "Selenium UI тесты")
    
    selenium_group.addoption(
        "--selenium-browser",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Браузер для Selenium тестов: chrome или firefox"
    )
    
    selenium_group.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск в headless режиме"
    )
    
    selenium_group.addoption(
        "--window-size",
        default="1920,1080",
        help="Размер окна браузера (ширина,высота)"
    )
    
    # Общие опции для всех тестов
    general_group = parser.getgroup("general", "Общие настройки тестов")
    
    general_group.addoption(
        "--base-url",
        default="https://www.chitai-gorod.ru",
        help="Базовый URL для тестирования"
    )
    
    general_group.addoption(
        "--retry-failed",
        action="store_true",
        default=False,
        help="Повторно запускать упавшие тесты"
    )
    
    general_group.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="Запускать медленные тесты"
    )
    
    # Опции для отчетов
    report_group = parser.getgroup("report", "Настройки отчетов")
    
    report_group.addoption(
        "--allure-dir",
        default="allure-results",
        help="Директория для отчетов Allure"
    )
    
    report_group.addoption(
        "--screenshot-on-fail",
        action="store_true",
        default=True,
        help="Делать скриншоты при падении тестов"
    )


@pytest.fixture(scope="function")
def browser(request):
    """Фикстура для запуска браузера в UI тестах"""
    
    # Получаем параметры из командной строки
    browser_name = request.config.getoption("--selenium-browser").lower()
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base-url")
    window_size = request.config.getoption("--window-size")
    
    driver = None
    
    try:
        if browser_name == "chrome":
            options = Options()
            
            if headless:
                options.add_argument("--headless=new")
            
            # Разбираем размер окна
            width, height = window_size.split(',')
            options.add_argument(f"--window-size={width},{height}")
            
            # Базовые опции для стабильности
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            
            # Настройки для обхода защиты от ботов
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # User-Agent для обхода защиты
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Дополнительные опции
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument("--disable-notifications")
            
            try:
                # Используем webdriver-manager для автоматической загрузки драйвера
                from selenium.webdriver.chrome.service import Service
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
            except Exception as e:
                # Резервный вариант - без service
                print(f"Ошибка при запуске Chrome через Service: {e}")
                print("Пробуем запустить Chrome без явного Service...")
                driver = webdriver.Chrome(options=options)
            
        elif browser_name == "firefox":
            options = FirefoxOptions()
            
            if headless:
                options.add_argument("--headless")
            
            # Настраиваем Firefox
            options.set_preference("general.useragent.override", 
                                 "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0")
            
            # Разбираем размер окна
            width, height = window_size.split(',')
            options.add_argument(f"--width={width}")
            options.add_argument(f"--height={height}")
            
            try:
                from selenium.webdriver.firefox.service import Service
                service = Service(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
            except Exception as e:
                # Резервный вариант
                print(f"Ошибка при запуске Firefox через Service: {e}")
                print("Пробуем запустить Firefox без явного Service...")
                driver = webdriver.Firefox(options=options)
        
        else:
            pytest.skip(f"Браузер {browser_name} не поддерживается. Используйте 'chrome' или 'firefox'")
        
        # Настройки драйвера
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)
        
        # Сохраняем конфигурацию в объекте драйвера для доступа в тестах
        driver.test_config = {
            'base_url': base_url,
            'browser': browser_name,
            'headless': headless,
            'window_size': window_size
        }
        
        yield driver
        
    except Exception as e:
        # Если не удалось запустить браузер
        error_msg = f"Не удалось запустить браузер {browser_name}: {str(e)}"
        print(f"DEBUG: {error_msg}")
        print(f"DEBUG: Python {sys.version}")
        print(f"DEBUG: Текущая директория: {os.getcwd()}")
        
        # Пробуем самый простой способ как запасной вариант
        try:
            if browser_name == "chrome":
                driver = webdriver.Chrome()
                driver.test_config = {'base_url': base_url, 'browser': browser_name}
                yield driver
                return
        except Exception as e2:
            print(f"DEBUG: Резервный метод также не сработал: {e2}")
        
        pytest.skip(f"Не удалось запустить браузер: {str(e)}")
    
    finally:
        # Закрытие браузера
        if driver:
            try:
                driver.quit()
            except:
                pass


@pytest.fixture(scope="function")
def chrome_options(request):
    """Фикстура для получения настроек Chrome"""
    from selenium.webdriver.chrome.options import Options
    options = Options()
    
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={request.config.getoption('--window-size')}")
    
    return options


@pytest.fixture(scope="session")
def api_base_url(request):
    """Фикстура для получения базового URL API тестов"""
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def request_headers():
    """Фикстура с заголовками для API запросов"""
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }


@pytest.fixture(scope="function")
def skip_slow(request):
    """Фикстура для пропуска медленных тестов если не указан флаг --slow"""
    if request.node.get_closest_marker('slow') and not request.config.getoption("--slow"):
        pytest.skip("Медленный тест пропущен. Используйте --slow для запуска.")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания отчетов Allure и обработки результатов тестов"""
    outcome = yield
    rep = outcome.get_result()
    
    # Сохраняем результат теста в item для доступа в фикстурах
    if rep.when == "call":
        item.test_result = rep
        
        # Если тест упал и включен retry, добавляем маркер для повторного запуска
        if rep.failed and item.config.getoption("--retry-failed"):
            if not hasattr(item, '_retry'):
                item._retry = 1
                # Помечаем для повторного запуска
                item.add_marker(pytest.mark.flaky(reruns=1, reruns_delay=1))
        
        # Делаем скриншот при падении UI тестов
        if (rep.failed and 
            item.config.getoption("--screenshot-on-fail") and
            "browser" in item.fixturenames):
            
            browser = item.funcargs.get("browser")
            if browser:
                try:
                    # Скриншот
                    screenshot = browser.get_screenshot_as_png()
                    allure.attach(
                        screenshot,
                        name="screenshot_on_failure",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                    # URL текущей страницы
                    current_url = browser.current_url
                    allure.attach(
                        current_url,
                        name="failed_page_url",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    # Исходный код страницы (первые 5000 символов)
                    try:
                        page_source = browser.page_source[:5000]
                        allure.attach(
                            page_source,
                            name="page_source_on_failure",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    except:
                        pass
                    
                    # Логи браузера (если доступны)
                    try:
                        logs = browser.get_log('browser')
                        if logs:
                            logs_text = "\n".join([str(log) for log in logs[-10:]])  # Последние 10 записей
                            allure.attach(
                                logs_text,
                                name="browser_logs",
                                attachment_type=allure.attachment_type.TEXT
                            )
                    except:
                        pass
                        
                except Exception as e:
                    allure.attach(
                        f"Не удалось сделать скриншот: {str(e)}",
                        name="screenshot_error",
                        attachment_type=allure.attachment_type.TEXT
                    )


def pytest_configure(config):
    """Конфигурация pytest при старте"""
    
    # Регистрация пользовательских меток
    config.addinivalue_line("markers", "ui: UI тесты (Selenium)")
    config.addinivalue_line("markers", "api: API тесты (HTTP запросы)")
    config.addinivalue_line("markers", "smoke: Smoke тесты")
    config.addinivalue_line("markers", "regression: Регрессионные тесты")
    config.addinivalue_line("markers", "search: Тесты поиска")
    config.addinivalue_line("markers", "cart: Тесты корзины")
    config.addinivalue_line("markers", "auth: Тесты авторизации")
    config.addinivalue_line("markers", "slow: Медленные тесты (требуют --slow)")
    config.addinivalue_line("markers", "flaky: Нестабильные тесты")
    
    # Настройка Allure если используется
    if config.getoption("--allure-dir"):
        allure_dir = config.getoption("--allure-dir")
        os.makedirs(allure_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print("НАСТРОЙКИ ТЕСТИРОВАНИЯ")
    print(f"{'='*60}")
    print(f"Базовый URL: {config.getoption('--base-url')}")
    print(f"Браузер для UI тестов: {config.getoption('--selenium-browser')}")
    print(f"Headless режим: {'Да' if config.getoption('--headless') else 'Нет'}")
    print(f"Размер окна: {config.getoption('--window-size')}")
    print(f"Повтор упавших тестов: {'Да' if config.getoption('--retry-failed') else 'Нет'}")
    print(f"Запуск медленных тестов: {'Да' if config.getoption('--slow') else 'Нет'}")
    print(f"{'='*60}\n")


def pytest_collection_modifyitems(config, items):
    """Модификация списка тестов перед запуском"""
    
    # Пропускаем медленные тесты если не указан флаг --slow
    if not config.getoption("--slow"):
        skip_slow = pytest.mark.skip(reason="Требуется флаг --slow для запуска медленных тестов")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    
    # Выводим информацию о собранных тестах
    print(f"\nНайдено тестов: {len(items)}")
    
    # Группируем тесты по типам
    ui_tests = [item for item in items if "ui" in item.keywords]
    api_tests = [item for item in items if "api" in item.keywords]
    smoke_tests = [item for item in items if "smoke" in item.keywords]
    
    if ui_tests:
        print(f"  UI тестов: {len(ui_tests)}")
    if api_tests:
        print(f"  API тестов: {len(api_tests)}")
    if smoke_tests:
        print(f"  Smoke тестов: {len(smoke_tests)}")
    
    print()