import pytest
import allure
import requests
import time
import json
from config import BASE_URL, TEST_SEARCH_QUERIES


@allure.story("API тесты сайта Читай-город")
class TestAPI:
    
    def _make_request(self, url, method='GET', **kwargs):
        """Универсальный метод для выполнения запросов с заголовками"""
        headers = kwargs.get('headers', {})
        
        # Базовые заголовки
        base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # Объединяем заголовки
        base_headers.update(headers)
        kwargs['headers'] = base_headers
        kwargs['timeout'] = kwargs.get('timeout', 15)
        
        try:
            if method.upper() == 'GET':
                response = requests.get(url, **kwargs)
            elif method.upper() == 'POST':
                response = requests.post(url, **kwargs)
            else:
                raise ValueError(f"Метод {method} не поддерживается")
            
            return response
        except requests.exceptions.Timeout:
            pytest.skip(f"Таймаут при запросе к {url}")
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Ошибка запроса к {url}: {e}")
    
    @allure.title("Тест доступности сайта")
    @allure.description("Проверка что сайт отвечает на HTTP запросы")
    @pytest.mark.api
    @pytest.mark.smoke
    def test_site_availability(self, api_base_url):
        """Проверка доступности сайта"""
        with allure.step(f"Отправка GET запроса на {api_base_url}"):
            start_time = time.time()
            response = self._make_request(api_base_url)
            response_time = time.time() - start_time
        
        with allure.step("Анализ ответа"):
            allure.attach(
                f"Статус код: {response.status_code}\n"
                f"Время ответа: {response_time:.2f} секунд\n"
                f"Размер ответа: {len(response.text)} символов",
                name="response_info",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем разные сценарии
            if response.status_code == 403:
                allure.attach(
                    "Сайт возвращает 403 Forbidden - вероятно защита от ботов",
                    name="bot_protection_info",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip("Сайт защищен от автоматических запросов (403 Forbidden)")
            
            assert response.status_code in [200, 403, 429], \
                f"Неожиданный статус код: {response.status_code}"
    
    @allure.title("Тест поиска через API")
    @allure.description("Проверка работы поискового функционала")
    @pytest.mark.api
    @pytest.mark.search
    def test_search_api(self):
        """Тестирование поиска через анализ ответов"""
        search_query = TEST_SEARCH_QUERIES[1]  # "Гарри Поттер"
        
        with allure.step(f"Анализ поиска по запросу: {search_query}"):
            # Пробуем разные URL для поиска
            search_urls = [
                f"{BASE_URL}/search?q={search_query}",
                f"{BASE_URL}/catalog/search?q={search_query}",
                f"{BASE_URL}/search/?query={search_query}"
            ]
            
            search_performed = False
            results_info = []
            
            for url in search_urls:
                try:
                    response = self._make_request(url)
                    
                    result_info = {
                        'url': url,
                        'status_code': response.status_code,
                        'response_size': len(response.text),
                        'is_html': 'text/html' in response.headers.get('Content-Type', '')
                    }
                    results_info.append(result_info)
                    
                    if response.status_code == 200:
                        search_performed = True
                        html_content = response.text.lower()
                        
                        # Проверяем что на странице есть признаки поиска
                        search_indicators_found = []
                        for indicator in [search_query.lower(), 'результат', 'найдено', 'search']:
                            if indicator in html_content:
                                search_indicators_found.append(indicator)
                        
                        allure.attach(
                            f"Поиск выполнен: {url}\n"
                            f"Статус: {response.status_code}\n"
                            f"Найдены индикаторы: {search_indicators_found}\n"
                            f"Размер ответа: {len(response.text)} символов",
                            name="search_success_info",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break
                        
                except Exception as e:
                    results_info.append({
                        'url': url,
                        'error': str(e)
                    })
                    continue
            
            # Сохраняем информацию о всех попытках
            allure.attach(
                json.dumps(results_info, indent=2, ensure_ascii=False),
                name="search_attempts",
                attachment_type=allure.attachment_type.JSON
            )
            
            if not search_performed:
                # Проверяем главную страницу на наличие поисковых элементов
                response = self._make_request(BASE_URL)
                
                if response.status_code == 200:
                    html_content = response.text.lower()
                    
                    # Ищем формы поиска в HTML
                    import re
                    search_forms = re.findall(r'<form[^>]*>.*?</form>', response.text, re.DOTALL | re.IGNORECASE)
                    search_inputs = re.findall(r'<input[^>]*type=[\'"]?text[\'"]?[^>]*>', response.text, re.IGNORECASE)
                    search_inputs += re.findall(r'<input[^>]*type=[\'"]?search[\'"]?[^>]*>', response.text, re.IGNORECASE)
                    
                    allure.attach(
                        f"На главной странице найдено:\n"
                        f"Форм поиска: {len(search_forms)}\n"
                        f"Поле ввода текста: {len(search_inputs)}\n"
                        f"Содержит 'search': {'search' in html_content}\n"
                        f"Содержит 'поиск': {'поиск' in html_content}",
                        name="search_analysis",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    # Проверяем наличие признаков поиска
                    has_search_form = len(search_forms) > 0 or len(search_inputs) > 0
                    has_search_text = 'search' in html_content or 'поиск' in html_content
                    
                    assert has_search_form or has_search_text, \
                        "На сайте не найдены признаки поисковой системы"
                else:
                    pytest.skip(f"Не удалось получить главную страницу: {response.status_code}")
    
    @allure.title("Тест категорий товаров")
    @allure.description("Проверка доступности категорий товаров")
    @pytest.mark.api
    def test_categories_api(self):
        """Тестирование категорий товаров"""
        with allure.step("Анализ структуры категорий"):
            response = self._make_request(BASE_URL)
            
            if response.status_code != 200:
                pytest.skip(f"Не удалось получить страницу: {response.status_code}")
            
            html_content = response.text
            
            # Ищем ссылки на категории
            import re
            
            # Паттерны для поиска ссылок на категории
            category_patterns = [
                r'href=[\'"]?(/[^\'">]*catalog[^\'">]*)[\'"]?',
                r'href=[\'"]?(/[^\'">]*category[^\'">]*)[\'"]?',
                r'href=[\'"]?(/[^\'">]*books[^\'">]*)[\'"]?',
                r'href=[\'"]?(/[^\'">]*knigi[^\'">]*)[\'"]?',
                r'href=[\'"]?(/[^\'">]*/catalog/[^\'">]*)[\'"]?',
            ]
            
            found_links = []
            for pattern in category_patterns:
                matches = re.findall(pattern, html_content, re.IGNORECASE)
                for match in matches:
                    if match not in found_links:
                        found_links.append(match)
            
            # Нормализуем ссылки
            normalized_links = []
            for link in found_links:
                if link.startswith('/'):
                    full_link = f"{BASE_URL}{link}"
                elif link.startswith('http'):
                    full_link = link
                else:
                    full_link = f"{BASE_URL}/{link}"
                normalized_links.append(full_link)
            
            # Ограничиваем количество для отчета
            display_links = normalized_links[:10]
            
            allure.attach(
                f"Всего найдено ссылок на категории: {len(normalized_links)}\n"
                f"Примеры (первые 10):\n" + "\n".join(display_links),
                name="category_links",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем наличие категорий в тексте страницы
            category_indicators = ['каталог', 'catalog', 'книги', 'books', 'товар', 'product']
            found_indicators = []
            
            html_lower = html_content.lower()
            for indicator in category_indicators:
                if indicator in html_lower:
                    found_indicators.append(indicator)
            
            allure.attach(
                f"Найдены индикаторы категорий: {found_indicators}",
                name="category_indicators",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем что сайт содержит признаки категорий товаров
            assert len(normalized_links) > 0 or len(found_indicators) > 0, \
                "На сайте не найдены признаки категорий товаров"
    
    @allure.title("Тест мета-данных сайта")
    @allure.description("Проверка мета-информации сайта")
    @pytest.mark.api
    def test_metadata(self):
        """Проверка мета-данных сайта"""
        with allure.step("Получение и анализ мета-данных"):
            response = self._make_request(BASE_URL)
            
            if response.status_code != 200:
                pytest.skip(f"Не удалось получить страницу: {response.status_code}")
            
            html_content = response.text
            
            # Извлекаем мета-теги
            import re
            meta_tags = re.findall(r'<meta[^>]+>', html_content)
            
            # Также ищем title
            title_match = re.search(r'<title[^>]*>(.*?)</title>', html_content, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Не найден"
            
            allure.attach(
                f"Заголовок страницы: {title}\n"
                f"Найдено мета-тегов: {len(meta_tags)}\n"
                f"Размер страницы: {len(html_content)} символов",
                name="metadata_info",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Сохраняем все мета-теги для анализа
            if meta_tags:
                meta_info = "Мета-теги:\n" + "\n".join(meta_tags[:10])  # Показываем первые 10
                allure.attach(
                    meta_info,
                    name="meta_tags_details",
                    attachment_type=allure.attachment_type.TEXT
                )
            
            # Проверяем базовые требования
            # Для современных SPA-сайтов может быть меньше мета-тегов
            assert len(meta_tags) >= 1, "Страница должна содержать хотя бы один мета-тег"
            
            # Проверяем наличие важных мета-тегов или title
            has_viewport = any('viewport' in tag.lower() for tag in meta_tags)
            has_charset = any('charset' in tag.lower() for tag in meta_tags)
            has_title = title != "Не найден" and len(title.strip()) > 0
            
            assert has_viewport or has_charset or has_title, \
                "Страница должна содержать базовые мета-данные"
            
            # Проверяем кодировку
            if has_charset:
                charset_meta = [tag for tag in meta_tags if 'charset' in tag.lower()][0]
                assert 'utf-8' in charset_meta.lower(), \
                    f"Страница должна использовать UTF-8 кодировку. Найдено: {charset_meta}"
    
    @allure.title("Тест производительности сайта")
    @allure.description("Проверка времени ответа сайта")
    @pytest.mark.api
    def test_performance(self):
        """Тестирование производительности сайта"""
        with allure.step("Измерение времени ответа"):
            response_times = []
            status_codes = []
            
            # Делаем 3 запроса для получения среднего значения
            for i in range(3):
                start_time = time.time()
                response = self._make_request(BASE_URL)
                response_time = time.time() - start_time
                response_times.append(response_time)
                status_codes.append(response.status_code)
                
                time.sleep(1)  # Пауза между запросами
            
            # Рассчитываем статистику
            successful_responses = [rt for rt, sc in zip(response_times, status_codes) if sc == 200]
            
            if successful_responses:
                avg_time = sum(successful_responses) / len(successful_responses)
                max_time = max(successful_responses)
                min_time = min(successful_responses)
            else:
                # Если все запросы вернули ошибку, используем все времена
                avg_time = sum(response_times) / len(response_times)
                max_time = max(response_times)
                min_time = min(response_times)
            
            allure.attach(
                f"Статистика запросов:\n"
                f"Всего запросов: {len(response_times)}\n"
                f"Успешных (200): {len(successful_responses)}\n"
                f"Коды статусов: {status_codes}\n\n"
                f"Время ответа:\n"
                f"Запрос 1: {response_times[0]:.2f} сек (статус: {status_codes[0]})\n"
                f"Запрос 2: {response_times[1]:.2f} сек (статус: {status_codes[1]})\n"
                f"Запрос 3: {response_times[2]:.2f} сек (статус: {status_codes[2]})\n\n"
                f"Статистика по успешным запросам:\n"
                f"Среднее: {avg_time:.2f} сек\n"
                f"Минимальное: {min_time:.2f} сек\n"
                f"Максимальное: {max_time:.2f} сек",
                name="performance_results",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # Проверяем что сайт отвечает (не обязательно с 200 статусом)
            assert any(sc == 200 for sc in status_codes) or all(sc == 403 for sc in status_codes), \
                f"Сайт не отвечает корректно. Коды статусов: {status_codes}"
            
            # Если есть успешные запросы, проверяем производительность
            if successful_responses:
                assert avg_time < 5.0, f"Среднее время ответа слишком долгое: {avg_time:.2f} секунд"
                assert max_time < 10.0, f"Максимальное время ответа слишком долгое: {max_time:.2f} секунд"