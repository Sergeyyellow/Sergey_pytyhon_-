import pytest
import requests
import json


class TestYougileProjectsAPI:
    
    # ==================== ПОЗИТИВНЫЕ ТЕСТЫ ====================
    
    def test_create_project_positive(self, base_url, headers, unique_title, cleanup_projects):

        url = f"{base_url}/projects"
        data = {
            "title": unique_title
        }
        response = requests.post(url, json=data, headers=headers)
        assert response.status_code in [200, 201], \
            f"Ожидался статус 200/201, получен {response.status_code}. Ответ: {response.text}"
        
        response_data = response.json()
        assert "id" in response_data, "В ответе должен быть id проекта"
    
        cleanup_projects.append(response_data["id"])
    
    def test_get_project_positive(self, base_url, headers, unique_title, cleanup_projects):

        create_url = f"{base_url}/projects"
        create_data = {"title": unique_title}
        create_response = requests.post(create_url, json=create_data, headers=headers)
        
        assert create_response.status_code in [200, 201], "Не удалось создать проект для теста"
        
        project_id = create_response.json()["id"]
        cleanup_projects.append(project_id)
    
        get_url = f"{base_url}/projects/{project_id}"
        response = requests.get(get_url, headers=headers)
    
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        
        response_data = response.json()
        assert response_data["id"] == project_id, "ID проекта должен совпадать"
    
    def test_update_project_positive(self, base_url, headers, unique_title, cleanup_projects):
    
        create_url = f"{base_url}/projects"
        create_data = {"title": unique_title}
        create_response = requests.post(create_url, json=create_data, headers=headers)
        
        assert create_response.status_code in [200, 201], "Не удалось создать проект для теста"
        
        project_id = create_response.json()["id"]
        cleanup_projects.append(project_id)
    
        update_url = f"{base_url}/projects/{project_id}"
        new_title = f"Updated {unique_title}"
        update_data = {"title": new_title}
        
        response = requests.put(update_url, json=update_data, headers=headers)
    
        assert response.status_code == 200, \
            f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
    
        get_response = requests.get(update_url, headers=headers)
        updated_project = get_response.json()
        assert updated_project["title"] == new_title, "Название проекта должно обновиться"
    
    # ==================== НЕГАТИВНЫЕ ТЕСТЫ ====================
    
    def test_create_project_negative_missing_title(self, base_url, headers):
    
        # Подготовка данных (без title)
        url = f"{base_url}/projects"
        data = {}  # Пустой объект, без title
    
        response = requests.post(url, json=data, headers=headers)
        assert response.status_code == 400, \
            f"Ожидалась ошибка 400 при отсутствии title, получен {response.status_code}"
    
    def test_get_project_negative_not_found(self, base_url, headers):

        # Используем несуществующий ID
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        url = f"{base_url}/projects/{non_existent_id}"
        response = requests.get(url, headers=headers)
    
        assert response.status_code in [400, 404], \
            f"Ожидалась ошибка 400/404 для несуществующего проекта, получен {response.status_code}"
    
    def test_update_project_negative_not_found(self, base_url, headers, unique_title):

        # Используем несуществующий ID
        non_existent_id = "00000000-0000-0000-0000-000000000000"
        url = f"{base_url}/projects/{non_existent_id}"
        data = {"title": unique_title}
        response = requests.put(url, json=data, headers=headers)
    
        assert response.status_code in [400, 404], \
            f"Ожидалась ошибка 400/404 для несуществующего проекта, получен {response.status_code}"
    
    # ==================== ДОПОЛНИТЕЛЬНЫЕ ТЕСТЫ ====================
    
    def test_create_project_negative_empty_title(self, base_url, headers):
    
        url = f"{base_url}/projects"
        data = {"title": ""}  # Пустая строка
        
        response = requests.post(url, json=data, headers=headers)
        
        assert response.status_code == 400, \
            f"Ожидалась ошибка 400 при пустом title, получен {response.status_code}"
    
    def test_update_project_negative_empty_title(self, base_url, headers, unique_title, cleanup_projects):
    
        create_url = f"{base_url}/projects"
        create_data = {"title": unique_title}
        create_response = requests.post(create_url, json=create_data, headers=headers)
        
        assert create_response.status_code in [200, 201]
        
        project_id = create_response.json()["id"]
        cleanup_projects.append(project_id)
        
        update_url = f"{base_url}/projects/{project_id}"
        update_data = {"title": ""}
        
        response = requests.put(update_url, json=update_data, headers=headers)
        
        assert response.status_code == 400, \
            f"Ожидалась ошибка 400 при пустом title в update, получен {response.status_code}"
    
    def test_project_lifecycle(self, base_url, headers, cleanup_projects):
    
        import time
    
        unique_title = f"Lifecycle Test {int(time.time())}"
        create_url = f"{base_url}/projects"
        create_data = {"title": unique_title}
        
        create_response = requests.post(create_url, json=create_data, headers=headers)
        assert create_response.status_code in [200, 201]
        
        project_id = create_response.json()["id"]
        cleanup_projects.append(project_id)
    
        get_url = f"{base_url}/projects/{project_id}"
        get_response = requests.get(get_url, headers=headers)
        assert get_response.status_code == 200
    
        new_title = f"Updated {unique_title}"
        update_data = {"title": new_title}
        update_response = requests.put(get_url, json=update_data, headers=headers)
        assert update_response.status_code == 200
    
        verify_response = requests.get(get_url, headers=headers)
        assert verify_response.status_code == 200
        verify_data = verify_response.json()
        assert verify_data["title"] == new_title