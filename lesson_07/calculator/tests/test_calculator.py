import sys
import os
import pytest
from selenium import webdriver

# Добавляем родительскую директорию в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from pages.calculator_page import CalculatorPage

class TestCalculator:
    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.calculator_page = CalculatorPage(self.driver)
    
    def teardown_method(self):
        self.driver.quit()
    
    def test_slow_calculator_addition(self):
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        self.calculator_page.set_delay(45)
        self.calculator_page.click_number(7)
        self.calculator_page.click_plus()
        self.calculator_page.click_number(8)
        self.calculator_page.click_equals()
        result = self.calculator_page.wait_for_result()
        assert result == "15", f"Ожидался результат '15', но получен '{result}'"