from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class CheckoutPage(BasePage):
    # Локаторы формы
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    
    # Локаторы итоговой страницы
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    
    def enter_first_name(self, first_name):
        """Вводит имя"""
        first_name_field = self.wait.until(
            EC.element_to_be_clickable(self.FIRST_NAME_INPUT)
        )
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        return self
    
    def enter_last_name(self, last_name):
        """Вводит фамилию"""
        last_name_field = self.driver.find_element(*self.LAST_NAME_INPUT)
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        return self
    
    def enter_postal_code(self, postal_code):
        """Вводит почтовый индекс"""
        postal_code_field = self.driver.find_element(*self.POSTAL_CODE_INPUT)
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        return self
    
    def fill_checkout_form(self, first_name, last_name, postal_code):
        """Заполняет всю форму оформления заказа"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
        return self
    
    def click_continue(self):
        """Нажимает кнопку Continue"""
        continue_button = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        continue_button.click()
    
    def get_total_amount(self):
        """Возвращает итоговую сумму"""
        total_element = self.wait.until(
            EC.presence_of_element_located(self.TOTAL_LABEL)
        )
        total_text = total_element.text
        # Извлекаем число из текста "Total: $58.29"
        return total_text.replace("Total: $", "")