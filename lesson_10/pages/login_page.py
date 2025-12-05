"""
Страница авторизации интернет-магазина.
"""
from selenium.webdriver.common.by import By
from .base_page import BasePage


class LoginPage(BasePage):
    """
    Класс для работы со страницей авторизации.
    """
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    
    def open(self) -> 'LoginPage':
        """
        Открывает страницу авторизации.
        
        Returns:
            LoginPage - текущий объект страницы
        """
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Вводит имя пользователя.
        
        Args:
            username: str - имя пользователя
            
        Returns:
            LoginPage - текущий объект страницы
        """
        username_field = self.driver.find_element(*self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)
        return self
    
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Вводит пароль.
        
        Args:
            password: str - пароль
            
        Returns:
            LoginPage - текущий объект страницы
        """
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login(self) -> None:
        """Нажимает кнопку входа."""
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
    
    def login(self, username: str, password: str) -> None:
        """
        Выполняет полный процесс авторизации.
        
        Args:
            username: str - имя пользователя
            password: str - пароль
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()