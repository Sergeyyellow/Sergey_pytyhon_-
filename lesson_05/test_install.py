try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    print("✅ Все зависимости установлены правильно!")
except ImportError as e:
    print(f"❌ Ошибка: {e}")