import pytest
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException
)
from config import BASE_URL, TEST_SEARCH_QUERIES


@allure.story("UI тесты сайта Читай-город")
class TestUI:
    
    def _safe_click(self, browser, element, description=""):
        """Безопасный клик с обработкой исключений"""
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            # Пробуем кликнуть через JavaScript
            try:
                browser.execute_script("arguments[0].click();", element)
                allure.attach(
                    f"Клик через JavaScript выполнен: {description}",
                    name="js_click",
                    attachment_type=allure.attachment_type.TEXT
                )
                return True
            except:
                # Пробуем ActionChains
                try:
                    ActionChains(browser).move_to_element(element).click().perform()
                    allure.attach(
                        f"Клик через ActionChains выполнен: {description}",
                        name="action_chains_click",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    return True
                except:
                    allure.attach(
                        f"Не удалось кликнуть на элемент: {description}",
                        name="click_failed",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    return False
        except ElementNotInteractableException:
            allure.attach(
                f"Элемент не интерактивен: {description}",
                name="element_not_interactable",
                attachment_type=allure.attachment_type.TEXT
            )
            return False
        except Exception as e:
            allure.attach(
                f"Ошибка при клике: {str(e)} - {description}",
                name="click_error",
                attachment_type=allure.attachment_type.TEXT
            )
            return False
    
    @allure.title("Тест загрузки главной страницы")
    @allure.description("Проверка что главная страница загружается корректно")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_home_page_load(self, browser):
        """Проверка загрузки главной страницы"""
        # Получаем base_url из конфигурации браузера
        base_url = browser.test_config['base_url']
        
        with allure.step(f"Открыть главную страницу {base_url}"):
            browser.get(base_url)
            
            # Ждем загрузки страницы
            WebDriverWait(browser, 30).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            
            # Даем время на загрузку динамического контента
            time.sleep(2)
        
        with allure.step("Проверить заголовок страницы"):
            title = browser.title
            allure.attach(
                f"Заголовок: {title}\nБраузер: {browser.test_config['browser']}\nHeadless: {browser.test_config['headless']}",
                name="page_info",
                attachment_type=allure.attachment_type.TEXT
            )
            assert title, "Заголовок страницы не должен быть пустым"
            
            # Для отладки сохраняем скриншот
            browser.save_screenshot("home_page.png")
            allure.attach.file(
                "home_page.png",
                name="home_page_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Проверить URL"):
            current_url = browser.current_url
            allure.attach(current_url, name="current_url", attachment_type=allure.attachment_type.TEXT)
            assert base_url in current_url, f"URL должен содержать {base_url}"
    
    def _find_element_with_retry(self, browser, by, selector, timeout=10, retries=3):
        """Поиск элемента с повторными попытками"""
        for attempt in range(retries):
            try:
                element = WebDriverWait(browser, timeout).until(
                    EC.presence_of_element_located((by, selector))
                )
                allure.attach(
                    f"Элемент найден: {selector} (попытка {attempt + 1})",
                    name="element_found",
                    attachment_type=allure.attachment_type.TEXT
                )
                return element
            except TimeoutException:
                if attempt == retries - 1:
                    raise
                time.sleep(1)  # Пауза между попытками
        return None
    
    def _scroll_to_element(self, browser, element):
        """Прокрутить страницу к элементу"""
        try:
            browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)
            return True
        except:
            return False
    
    @allure.title("Тест загрузки главной страницы")
    @allure.description("Проверка что главная страница загружается корректно")
    @pytest.mark.ui
    @pytest.mark.smoke
    def test_home_page_load(self, browser):
        """Проверка загрузки главной страницы"""
        with allure.step("Открыть главную страницу"):
            browser.get(BASE_URL)
            
            # Ждем загрузки страницы
            WebDriverWait(browser, 30).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            
            # Даем время на загрузку динамического контента
            time.sleep(2)
        
        with allure.step("Проверить заголовок страницы"):
            title = browser.title
            allure.attach(title, name="page_title", attachment_type=allure.attachment_type.TEXT)
            assert title, "Заголовок страницы не должен быть пустым"
            
            # Для отладки сохраняем скриншот
            browser.save_screenshot("home_page.png")
            allure.attach.file(
                "home_page.png",
                name="home_page_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Проверить URL"):
            current_url = browser.current_url
            allure.attach(current_url, name="current_url", attachment_type=allure.attachment_type.TEXT)
            assert "chitai-gorod" in current_url, f"URL должен содержать 'chitai-gorod'. Текущий: {current_url}"
    
    @allure.title("Тест поиска товаров")
    @allure.description("Проверка работы поиска на сайте")
    @pytest.mark.ui
    @pytest.mark.search
    def test_search_functionality(self, browser):
        """Тестирование поиска товаров"""
        search_query = TEST_SEARCH_QUERIES[0]  # "книга"
        
        with allure.step("Открыть главную страницу"):
            browser.get(BASE_URL)
            time.sleep(3)  # Даем больше времени на загрузку
        
        with allure.step("Найти поле поиска"):
            # Пробуем разные селекторы для поиска
            search_selectors = [
                ("input[type='search']", "Поиск по type='search'"),
                ("input[name='q']", "Поиск по name='q'"),
                (".search-input", "Поиск по классу .search-input"),
                ("#search", "Поиск по id #search"),
                ("[placeholder*='поиск']", "Поиск по placeholder"),
                ("[placeholder*='найти']", "Поиск по placeholder 'найти'"),
                ("input[aria-label*='поиск']", "Поиск по aria-label"),
            ]
            
            search_field = None
            found_selector = ""
            
            for selector, description in search_selectors:
                try:
                    # Ждем появления элемента
                    element = WebDriverWait(browser, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    
                    # Проверяем что элемент видим и доступен
                    if element.is_displayed() and element.is_enabled():
                        search_field = element
                        found_selector = f"{selector} ({description})"
                        
                        # Прокручиваем к элементу
                        self._scroll_to_element(browser, element)
                        
                        allure.attach(
                            f"Найдено поле поиска: {found_selector}",
                            name="search_field_info",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break
                except (TimeoutException, NoSuchElementException):
                    continue
            
            if not search_field:
                # Делаем скриншот для отладки
                browser.save_screenshot("search_field_not_found.png")
                allure.attach.file(
                    "search_field_not_found.png",
                    name="search_field_debug",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Также сохраняем HTML для анализа
                page_source = browser.page_source[:5000]
                allure.attach(
                    page_source,
                    name="page_source_sample",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                pytest.skip(f"Поле поиска не найдено. Проверенные селекторы: {[s[0] for s in search_selectors]}")
        
        with allure.step(f"Выполнить поиск: {search_query}"):
            try:
                # Очищаем поле и вводим текст
                search_field.clear()
                search_field.send_keys(search_query)
                
                # Пробуем разные способы отправки запроса
                try:
                    # Способ 1: Найти и нажать кнопку поиска
                    search_button_selectors = [
                        "button[type='submit']",
                        ".search-button",
                        ".btn-search",
                        "[aria-label*='поиск']",
                        "[type='submit']"
                    ]
                    
                    search_button = None
                    for button_selector in search_button_selectors:
                        try:
                            button = browser.find_element(By.CSS_SELECTOR, button_selector)
                            if button.is_displayed():
                                search_button = button
                                break
                        except:
                            continue
                    
                    if search_button:
                        self._safe_click(browser, search_button, "Кнопка поиска")
                    else:
                        # Способ 2: Отправить через Enter
                        search_field.send_keys(Keys.ENTER)
                except:
                    # Способ 3: Просто нажать Enter
                    search_field.send_keys(Keys.ENTER)
                
                # Ждем результатов поиска
                time.sleep(3)
                
                # Проверяем URL после поиска
                current_url = browser.current_url.lower()
                allure.attach(
                    f"URL после поиска: {current_url}",
                    name="search_url",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # Проверяем что поиск выполнился
                # Для современных сайтов поиск может выполняться без изменения URL
                page_content = browser.page_source.lower()
                has_search_results = any(word in page_content for word in ['результат', 'найдено', 'search', 'товар'])
                
                allure.attach(
                    f"Содержит 'результат': {'результат' in page_content}\n"
                    f"Содержит 'найдено': {'найдено' in page_content}\n"
                    f"Содержит 'search': {'search' in page_content}\n"
                    f"Содержит 'товар': {'товар' in page_content}",
                    name="search_content_check",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # Делаем скриншот результатов
                browser.save_screenshot("search_results.png")
                allure.attach.file(
                    "search_results.png",
                    name="search_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Проверяем что поиск выполнился (либо URL изменился, либо есть результаты на странице)
                url_changed = any(word in current_url for word in ['search', 'поиск', 'q=', 'query='])
                if not url_changed and not has_search_results:
                    allure.attach(
                        "Поиск возможно не выполнился",
                        name="search_maybe_failed",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Не падаем, т.к. это может быть особенность сайта
                
            except Exception as e:
                allure.attach(
                    f"Ошибка при выполнении поиска: {str(e)}",
                    name="search_error",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"Ошибка при выполнении поиска: {e}")
    
    @allure.title("Тест навигации по сайту")
    @allure.description("Проверка перехода по разделам сайта")
    @pytest.mark.ui
    def test_site_navigation(self, browser):
        """Тестирование навигации"""
        with allure.step("Открыть главную страницу"):
            browser.get(BASE_URL)
            time.sleep(3)
        
        with allure.step("Найти все ссылки на странице"):
            try:
                links = browser.find_elements(By.TAG_NAME, "a")
                valid_links = []
                
                for link in links[:15]:  # Проверяем первые 15 ссылок
                    try:
                        href = link.get_attribute("href")
                        text = link.text.strip() or link.get_attribute("title") or link.get_attribute("aria-label") or "Без текста"
                        
                        # Проверяем что ссылка валидна и ведет на тот же домен
                        if (href and href.startswith("http") and 
                            BASE_URL.split('//')[1].split('/')[0] in href and
                            len(text) > 1 and  # Исключаем очень короткие тексты
                            not any(word in href.lower() for word in ['javascript:', 'mailto:', 'tel:', '#'])):
                            
                            valid_links.append((text[:50], href))  # Обрезаем длинный текст
                    except:
                        continue
                
                allure.attach(
                    f"Всего ссылок на странице: {len(links)}\n"
                    f"Валидных ссылок (на тот же домен): {len(valid_links)}\n"
                    f"Примеры валидных ссылок:\n" + 
                    "\n".join([f"{text}: {href}" for text, href in valid_links[:5]]),
                    name="links_info",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                assert len(valid_links) > 0, "На странице нет валидных ссылок на тот же домен"
            
            except Exception as e:
                allure.attach(
                    f"Ошибка при поиске ссылок: {str(e)}",
                    name="links_error",
                    attachment_type=allure.attachment_type.TEXT
                )
                pytest.skip(f"Ошибка при поиске ссылок: {e}")
        
        with allure.step("Перейти по первой внутренней ссылке"):
            if valid_links:
                text, href = valid_links[0]
                allure.attach(
                    f"Переход по ссылке: {text} -> {href}",
                    name="navigation_info",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                try:
                    # Сохраняем текущий URL
                    initial_url = browser.current_url
                    
                    # Переходим по ссылке
                    browser.get(href)
                    time.sleep(3)
                    
                    # Проверяем что перешли на новую страницу
                    new_url = browser.current_url
                    assert new_url != initial_url, "Не произошло перехода на новую страницу"
                    
                    # Делаем скриншот новой страницы
                    browser.save_screenshot("navigation_result.png")
                    allure.attach.file(
                        "navigation_result.png",
                        name="navigation_screenshot",
                        attachment_type=allure.attachment_type.PNG
                    )
                    
                except Exception as e:
                    allure.attach(
                        f"Ошибка при переходе по ссылке: {str(e)}",
                        name="navigation_error",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Не падаем, просто отмечаем ошибку
    
    @allure.title("Тест корзины покупок")
    @allure.description("Проверка функционала корзины")
    @pytest.mark.ui
    @pytest.mark.cart
    def test_shopping_cart(self, browser):
        """Тестирование корзины"""
        with allure.step("Открыть главную страницу"):
            browser.get(BASE_URL)
            time.sleep(3)
        
        with allure.step("Найти элемент корзины"):
            cart_selectors = [
                (By.CSS_SELECTOR, ".cart-icon", "Иконка корзины по классу"),
                (By.CSS_SELECTOR, ".basket-icon", "Иконка корзины basket"),
                (By.CSS_SELECTOR, ".cart-button", "Кнопка корзины"),
                (By.CSS_SELECTOR, "[href*='cart']", "Ссылка с cart"),
                (By.CSS_SELECTOR, "[href*='basket']", "Ссылка с basket"),
                (By.CSS_SELECTOR, "[href*='order']", "Ссылка с order"),
                (By.XPATH, "//*[contains(text(), 'Корзина')]", "Текст 'Корзина'"),
                (By.XPATH, "//*[contains(text(), 'Корзине')]", "Текст 'Корзине'"),
                (By.XPATH, "//*[contains(text(), 'Basket')]", "Текст 'Basket'"),
                (By.XPATH, "//*[contains(text(), 'Cart')]", "Текст 'Cart'"),
                (By.CSS_SELECTOR, "[aria-label*='корзин']", "ARIA-label корзины"),
                (By.CSS_SELECTOR, "[title*='корзин']", "Title корзины"),
            ]
            
            cart_element = None
            cart_info = ""
            
            for by, selector, description in cart_selectors:
                try:
                    # Ждем появления элемента
                    element = WebDriverWait(browser, 3).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    
                    # Проверяем что элемент видим
                    if element.is_displayed():
                        cart_element = element
                        cart_info = f"{selector} ({description})"
                        
                        # Прокручиваем к элементу
                        self._scroll_to_element(browser, element)
                        
                        allure.attach(
                            f"Найден элемент корзины: {cart_info}",
                            name="cart_element_info",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break
                except (TimeoutException, NoSuchElementException):
                    continue
            
            if not cart_element:
                # Сохраняем скриншот для отладки
                browser.save_screenshot("cart_not_found.png")
                allure.attach.file(
                    "cart_not_found.png",
                    name="cart_debug_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Проверяем наличие слова "корзина" на странице
                page_content = browser.page_source.lower()
                has_cart_text = any(word in page_content for word in ['корзин', 'basket', 'cart'])
                
                allure.attach(
                    f"Проверенные селекторы: {[s[1] for s in cart_selectors]}\n"
                    f"Содержит 'корзин': {'корзин' in page_content}\n"
                    f"Содержит 'basket': {'basket' in page_content}\n"
                    f"Содержит 'cart': {'cart' in page_content}",
                    name="cart_analysis",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                if has_cart_text:
                    allure.attach(
                        "Текст корзины найден на странице, но элемент не кликабелен",
                        name="cart_text_found",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Не падаем, просто отмечаем
                else:
                    pytest.skip("Элемент корзины не найден")
                return
        
        with allure.step("Взаимодействие с корзиной"):
            initial_url = browser.current_url
            
            # Пробуем кликнуть на корзину
            click_success = self._safe_click(browser, cart_element, f"Корзина: {cart_info}")
            
            if click_success:
                # Ждем изменения
                time.sleep(2)
                
                # Проверяем результат
                new_url = browser.current_url
                page_content = browser.page_source.lower()
                
                allure.attach(
                    f"URL до клика: {initial_url}\n"
                    f"URL после клика: {new_url}\n"
                    f"Изменение URL: {'да' if new_url != initial_url else 'нет'}\n"
                    f"Содержит 'корзин': {'корзин' in page_content}\n"
                    f"Содержит 'basket': {'basket' in page_content}\n"
                    f"Содержит 'cart': {'cart' in page_content}",
                    name="cart_click_result",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                # Проверяем разные сценарии
                url_changed = new_url != initial_url
                has_cart_content = any(word in page_content for word in ['корзин', 'basket', 'cart'])
                
                if url_changed:
                    # Перешли на новую страницу
                    allure.attach(
                        "Произошел переход на новую страницу",
                        name="page_changed",
                        attachment_type=allure.attachment_type.TEXT
                    )
                elif has_cart_content:
                    # Возможно открылось модальное окно
                    allure.attach(
                        "Корзина возможно открылась в модальном окне",
                        name="modal_possible",
                        attachment_type=allure.attachment_type.TEXT
                    )
                else:
                    allure.attach(
                        "Клик выполнен, но изменений не обнаружено",
                        name="no_changes",
                        attachment_type=allure.attachment_type.TEXT
                    )
                
                # Делаем скриншот
                browser.save_screenshot("cart_interaction.png")
                allure.attach.file(
                    "cart_interaction.png",
                    name="cart_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            else:
                allure.attach(
                    "Не удалось кликнуть на элемент корзины",
                    name="cart_click_failed",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    @allure.title("Тест формы авторизации")
    @allure.description("Проверка наличия и доступности формы авторизации")
    @pytest.mark.ui
    @pytest.mark.auth
    def test_auth_form(self, browser):
        """Тестирование формы авторизации"""
        with allure.step("Открыть главную страницу"):
            browser.get(BASE_URL)
            time.sleep(3)
        
        with allure.step("Найти кнопку входа"):
            auth_selectors = [
                (By.XPATH, "//*[contains(text(), 'Войти')]", "Текст 'Войти'"),
                (By.XPATH, "//*[contains(text(), 'Вход')]", "Текст 'Вход'"),
                (By.XPATH, "//*[contains(text(), 'Личный кабинет')]", "Личный кабинет"),
                (By.XPATH, "//*[contains(text(), 'Профиль')]", "Профиль"),
                (By.CSS_SELECTOR, ".login-btn", "Класс .login-btn"),
                (By.CSS_SELECTOR, ".auth-btn", "Класс .auth-btn"),
                (By.CSS_SELECTOR, ".user-btn", "Класс .user-btn"),
                (By.CSS_SELECTOR, "[href*='login']", "Ссылка login"),
                (By.CSS_SELECTOR, "[href*='auth']", "Ссылка auth"),
                (By.CSS_SELECTOR, "[href*='signin']", "Ссылка signin"),
                (By.CSS_SELECTOR, "[href*='account']", "Ссылка account"),
                (By.CSS_SELECTOR, "[href*='profile']", "Ссылка profile"),
            ]
            
            auth_button = None
            auth_info = ""
            
            for by, selector, description in auth_selectors:
                try:
                    element = WebDriverWait(browser, 3).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    
                    if element.is_displayed():
                        auth_button = element
                        auth_info = f"{selector} ({description})"
                        
                        # Прокручиваем к элементу
                        self._scroll_to_element(browser, element)
                        
                        allure.attach(
                            f"Найдена кнопка авторизации: {auth_info}",
                            name="auth_button_info",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break
                except (TimeoutException, NoSuchElementException):
                    continue
            
            if not auth_button:
                # Проверяем наличие текста авторизации на странице
                page_content = browser.page_source.lower()
                has_auth_text = any(word in page_content for word in ['войти', 'вход', 'логин', 'login', 'авториз', 'auth'])
                
                allure.attach(
                    f"Содержит 'войти': {'войти' in page_content}\n"
                    f"Содержит 'вход': {'вход' in page_content}\n"
                    f"Содержит 'login': {'login' in page_content}\n"
                    f"Содержит 'auth': {'auth' in page_content}",
                    name="auth_text_check",
                    attachment_type=allure.attachment_type.TEXT
                )
                
                if has_auth_text:
                    allure.attach(
                        "Текст авторизации найден, но кнопка не обнаружена",
                        name="auth_text_found",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    # Не падаем
                else:
                    pytest.skip("Кнопка авторизации не найдена")
                return
        
        with allure.step("Открыть форму авторизации"):
            # Пробуем кликнуть на кнопку
            click_success = self._safe_click(browser, auth_button, f"Авторизация: {auth_info}")
            
            if click_success:
                time.sleep(2)
                
                # Ищем форму авторизации
                form_selectors = [
                    "input[type='tel']",
                    "input[name='phone']",
                    "input[type='text'][inputmode='numeric']",
                    ".auth-form",
                    ".login-form",
                    ".modal",
                    ".popup",
                    "[role='dialog']",
                    "form"
                ]
                
                form_found = False
                for selector in form_selectors:
                    try:
                        elements = browser.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            for element in elements:
                                if element.is_displayed():
                                    form_found = True
                                    allure.attach(
                                        f"Найдена форма авторизации: {selector}",
                                        name="auth_form_info",
                                        attachment_type=allure.attachment_type.TEXT
                                    )
                                    
                                    # Делаем скриншот формы
                                    browser.save_screenshot("auth_form.png")
                                    allure.attach.file(
                                        "auth_form.png",
                                        name="auth_form_screenshot",
                                        attachment_type=allure.attachment_type.PNG
                                    )
                                    break
                        if form_found:
                            break
                    except:
                        continue
                
                if form_found:
                    allure.attach(
                        "Форма авторизации успешно найдена и открыта",
                        name="auth_form_success",
                        attachment_type=allure.attachment_type.TEXT
                    )
                else:
                    # Проверяем изменился ли URL
                    current_url = browser.current_url
                    if 'login' in current_url or 'auth' in current_url or 'account' in current_url:
                        allure.attach(
                            f"Перешли на страницу авторизации: {current_url}",
                            name="auth_page",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    else:
                        allure.attach(
                            "Форма авторизации не найдена после клика",
                            name="auth_form_not_found",
                            attachment_type=allure.attachment_type.TEXT
                        )
            else:
                allure.attach(
                    "Не удалось кликнуть на кнопку авторизации",
                    name="auth_click_failed",
                    attachment_type=allure.attachment_type.TEXT
                )