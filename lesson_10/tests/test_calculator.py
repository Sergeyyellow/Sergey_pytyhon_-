import sys
import os
import pytest
import allure

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from pages.calculator_page import CalculatorPage

@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.CRITICAL)
class TestCalculator:
    """
    Тесты для функциональности калькулятора.
    """
    
    @allure.title("Тест сложения с задержкой")
    @allure.description("Проверка сложения 7 + 8 с задержкой 45 секунд")
    @allure.story("Медленные вычисления")
    @pytest.mark.slow
    def test_slow_calculator_addition(self, driver):
    
        calculator_page = CalculatorPage(driver)
        
        with allure.step("Открыть страницу калькулятора"):
            driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        
        with allure.step("Установить задержку 45 секунд"):
            calculator_page.set_delay(45)
        
        with allure.step("Выполнить операцию 7 + 8"):
            calculator_page.click_number(7)
            calculator_page.click_plus()
            calculator_page.click_number(8)
            calculator_page.click_equals()
        
        with allure.step("Дождаться результата вычислений"):
            result = calculator_page.wait_for_result()
            allure.attach(f"Полученный результат: {result}", name="Результат вычислений")
        
        with allure.step("Проверить, что результат равен 15"):
            assert result == "15", f"Ожидался результат '15', но получен '{result}'"