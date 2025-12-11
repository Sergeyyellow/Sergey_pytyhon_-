import os
from dotenv import load_dotenv

load_dotenv()

# Базовые настройки из .env или значения по умолчанию
BASE_URL = os.getenv("BASE_URL", "https://www.chitai-gorod.ru")

# Настройки браузера
DEFAULT_BROWSER = os.getenv("BROWSER", "chrome")
HEADLESS = os.getenv("HEADLESS", "False").lower() == "true"
WINDOW_SIZE = os.getenv("WINDOW_SIZE", "1920,1080")

# Настройки времени ожидания
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "30"))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "60"))

# Настройки запросов
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
REQUEST_RETRIES = int(os.getenv("REQUEST_RETRIES", "3"))

# Тестовые данные
TEST_SEARCH_QUERIES = ["книга", "Гарри Поттер", "Python", "детектив", "фантастика"]
TEST_PHONE = os.getenv("TEST_PHONE", "")