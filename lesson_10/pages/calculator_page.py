"""
Страница калькулятора с медленными вычислениями.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .base_page import BasePage


class CalculatorPage(BasePage):
    """
    Класс для работы со страницей калькулятора.
    """
    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    DISPLAY = (By.CSS_SELECTOR, ".screen")

    BUTTON_0 = (By.XPATH, "//span[text()='0']")
    BUTTON_1 = (By.XPATH, "//span[text()='1']")
    BUTTON_2 = (By.XPATH, "//span[text()='2']")
    BUTTON_3 = (By.XPATH, "//span[text()='3']")
    BUTTON_4 = (By.XPATH, "//span[text()='4']")
    BUTTON_5 = (By.XPATH, "//span[text()='5']")
    BUTTON_6 = (By.XPATH, "//span[text()='6']")
    BUTTON_7 = (By.XPATH, "//span[text()='7']")
    BUTTON_8 = (By.XPATH, "//span[text()='8']")
    BUTTON_9 = (By.XPATH, "//span[text()='9']")

    BUTTON_PLUS = (By.XPATH, "//span[text()='+']")
    BUTTON_MINUS = (By.XPATH, "//span[text()='-']")
    BUTTON_MULTIPLY = (By.XPATH, "//span[text()='×']")
    BUTTON_DIVIDE = (By.XPATH, "//span[text()='÷']")
    BUTTON_EQUALS = (By.XPATH, "//span[text()='=']")
    
    def set_delay(self, delay_seconds: int) -> None:
        """
        Устанавливает значение задержки в поле ввода.
        
        Args:
            delay_seconds: int - количество секунд задержки
        """
        delay_input = self.driver.find_element(*self.DELAY_INPUT)
        delay_input.clear()
        delay_input.send_keys(str(delay_seconds))
    
    def click_button(self, button_locator: tuple) -> None:
        """
        Нажимает указанную кнопку.
        
        Args:
            button_locator: tuple - локатор кнопки (By, значение)
        """
        button = self.driver.find_element(*button_locator)
        button.click()
    
    def click_number(self, number: int) -> None:
        """
        Нажимает кнопку с указанной цифрой.
        
        Args:
            number: int - цифра от 0 до 9
        """
        number_buttons = {
            0: self.BUTTON_0,
            1: self.BUTTON_1,
            2: self.BUTTON_2,
            3: self.BUTTON_3,
            4: self.BUTTON_4,
            5: self.BUTTON_5,
            6: self.BUTTON_6,
            7: self.BUTTON_7,
            8: self.BUTTON_8,
            9: self.BUTTON_9
        }
        self.click_button(number_buttons[number])
    
    def click_plus(self) -> None:
        """Нажимает кнопку плюс."""
        self.click_button(self.BUTTON_PLUS)
    
    def click_equals(self) -> None:
        """Нажимает кнопку равно."""
        self.click_button(self.BUTTON_EQUALS)
    
    def get_display_text(self) -> str:
        """
        Возвращает текст с дисплея калькулятора.
        
        Returns:
            str - текст с дисплея
        """
        display = self.driver.find_element(*self.DISPLAY)
        return display.text
    
    def wait_for_result(self, timeout: int = 50) -> str:
        """
        Ожидает появления результата на дисплее.
        
        Args:
            timeout: int - максимальное время ожидания в секундах
            
        Returns:
            str - результат вычислений
        """
        start_time = time.time()
        last_text = self.get_display_text()
        
        while time.time() - start_time < timeout:
            current_text = self.get_display_text()
            if current_text != last_text and current_text.isdigit():
                return current_text
            last_text = current_text
            time.sleep(0.5)
        
        return self.get_display_text()