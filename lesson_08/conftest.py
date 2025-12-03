import pytest
import requests
import time


@pytest.fixture
def base_url():
    return "https://ru.yougile.com/api-v2"


@pytest.fixture
def headers():
    """НАСТАВНИКУ: Заменить YOUR_TOKEN_HERE и YOUR_COMPANY_ID на реальные значения"""
    token = "YOUR_TOKEN_HERE"
    company_id = "YOUR_COMPANY_ID"
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Company-Id": company_id
    }


@pytest.fixture
def unique_title():
    """Генерация уникального названия для тестов"""
    return f"Test Project {int(time.time())}"


@pytest.fixture
def cleanup_projects():
    """Фикстура для очистки созданных проектов"""
    created_ids = []
    yield created_ids
    
    # Очистка после всех тестов
    for project_id in created_ids:
        try:
            requests.delete(
                f"https://ru.yougile.com/api-v2/projects/{project_id}",
                headers=headers()
            )
        except:
            pass