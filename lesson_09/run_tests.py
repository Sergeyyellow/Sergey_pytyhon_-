"""
Скрипт для запуска тестов с предварительной настройкой
"""
import subprocess
import sys
import os
from pathlib import Path

def check_dependencies():
    """Проверяем установлены ли зависимости"""
    try:
        import pytest
        import sqlalchemy
        import psycopg2
        print("✓ Все зависимости установлены")
        return True
    except ImportError as e:
        print(f"✗ Отсутствует зависимость: {e}")
        print("Установите зависимости: pip install -r requirements.txt")
        return False

def check_connection_params():
    """Проверяем параметры подключения"""
    conftest_path = Path(__file__).parent / "conftest.py"
    if not conftest_path.exists():
        print("✗ Файл conftest.py не найден")
        return False
    
    with open(conftest_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Проверяем, что параметры не стандартные
    if "mypassword" in content and "myuser" in content:
        print("⚠ ВНИМАНИЕ: Используются стандартные параметры подключения")
        print("Отредактируйте conftest.py с вашими реальными данными")
        print("DB_USER = 'ваш_пользователь'")
        print("DB_PASSWORD = 'ваш_пароль'")
        print("DB_NAME = 'ваша_база'")
        return False
    
    print("✓ Параметры подключения настроены")
    return True

def main():
    """Основная функция"""
    print("=" * 60)
    print("ЗАПУСК ТЕСТОВ ДЛЯ УРОКА 9")
    print("=" * 60)
    
    # Проверяем зависимости
    if not check_dependencies():
        sys.exit(1)
    
    # Проверяем параметры подключения
    check_connection_params()
    
    print("\n" + "=" * 60)
    print("ЗАПУСК PYTESTS...")
    print("=" * 60)
    
    # Запускаем тесты
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "test_crud_operations.py",
        "test_models.py"
    ])
    
    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("✗ НЕКОТОРЫЕ ТЕСТЫ НЕ ПРОШЛИ")
    
    print("=" * 60)
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()