"""
Страница оформления заказа интернет-магазина.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class CheckoutPage(BasePage):
    """
    Класс для работы со страницей оформления заказа.
    """

    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    
    def enter_first_name(self, first_name: str) -> 'CheckoutPage':
        """
        Вводит имя.
        
        Args:
            first_name: str - имя покупателя
            
        Returns:
            CheckoutPage - текущий объект страницы
        """
        first_name_field = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_NAME_INPUT)
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        return self
    
    def enter_last_name(self, last_name: str) -> 'CheckoutPage':
        """
        Вводит фамилию.
        
        Args:
            last_name: str - фамилия покупателя
            
        Returns:
            CheckoutPage - текущий объект страницы
        """
        last_name_field = self.driver.find_element(*self.LAST_NAME_INPUT)
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        return self
    
    def enter_postal_code(self, postal_code: str) -> 'CheckoutPage':
        """
        Вводит почтовый индекс.
        
        Args:
            postal_code: str - почтовый индекс
            
        Returns:
            CheckoutPage - текущий объект страницы
        """
        postal_code_field = self.driver.find_element(*self.POSTAL_CODE_INPUT)
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        return self
    
    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str) -> 'CheckoutPage':
        """
        Заполняет всю форму оформления заказа.
        
        Args:
            first_name: str - имя покупателя
            last_name: str - фамилия покупателя
            postal_code: str - почтовый индекс
            
        Returns:
            CheckoutPage - текущий объект страницы
        """
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self
    
    def click_continue(self) -> None:
        """Нажимает кнопку Continue."""
        continue_button = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        continue_button.click()
    
    def get_total_amount(self) -> str:
        """
        Возвращает итоговую сумму.
        
        Returns:
            str - итоговая сумма без символа валюты
        """
        total_element = self.wait.until(
            EC.presence_of_element_located(self.TOTAL_LABEL)
        )
        total_text = total_element.text
        return total_text.replace("Total: $", "")