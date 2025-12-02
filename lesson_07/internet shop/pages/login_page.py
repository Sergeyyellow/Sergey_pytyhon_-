from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    # Локаторы
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    
    def open(self):
        """Открывает страницу авторизации"""
        self.driver.get("https://www.saucedemo.com/")
        return self
    
    def enter_username(self, username):
        """Вводит имя пользователя"""
        username_field = self.driver.find_element(*self.USERNAME_INPUT)
        username_field.clear()
        username_field.send_keys(username)
        return self
    
    def enter_password(self, password):
        """Вводит пароль"""
        password_field = self.driver.find_element(*self.PASSWORD_INPUT)
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_login(self):
        """Нажимает кнопку входа"""
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()
    
    def login(self, username, password):
        """Выполняет полный процесс авторизации"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()