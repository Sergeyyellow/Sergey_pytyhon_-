import pytest
from string_utils import StringUtils

class TestStringUtils:
    
    @pytest.fixture
    def utils(self):
        return StringUtils()
    
    # Тесты для capitilize
    @pytest.mark.parametrize("input_str, expected", [
        ("skypro", "Skypro"),
        ("Skypro", "Skypro"),
        ("123abc", "123abc"),
        ("", ""),
        (" hello", " hello"),
        ("HELLO", "Hello"),
        ("a", "A"),
        (" test test", " test test")
    ])
    def test_capitilize_positive(self, utils, input_str, expected):
        assert utils.capitilize(input_str) == expected
    
    # Тесты для trim
    @pytest.mark.parametrize("input_str, expected", [
        ("   skypro", "skypro"),
        ("skypro", "skypro"),
        ("   ", ""),
        ("", ""),
        ("  hello world  ", "hello world  "),
        (" \t\nskypro", "\t\nskypro"),  # Не удаляет табы и переносы
        ("  a", "a")
    ])
    def test_trim_positive(self, utils, input_str, expected):
        assert utils.trim(input_str) == expected
    
    # Тесты для contains
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "S", True),
        ("SkyPro", "U", False),
        ("", "a", False),
        ("hello", "", True),  # Дефект: пустая строка всегда содержится
        ("test", "t", True),
        ("test", "T", False),
        ("123", "2", True),
        ("  space", " ", True)
    ])
    def test_contains(self, utils, string, symbol, expected):
        assert utils.contains(string, symbol) == expected
    
    # Тесты для delete_symbol
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "k", "SyPro"),
        ("SkyPro", "Pro", "Sky"),
        ("hello", "l", "heo"),
        ("test", "x", "test"),
        ("", "a", ""),
        ("aaa", "a", ""),
        ("banana", "na", "ba"),
        ("spaces here", " ", "spaceshere")
    ])
    def test_delete_symbol(self, utils, string, symbol, expected):
        assert utils.delete_symbol(string, symbol) == expected
    
    # Тесты для starts_with
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "S", True),
        ("SkyPro", "P", False),
        ("", "a", False),
        ("hello", "", True),  # Дефект: пустая строка всегда в начале
        (" test", " ", True),
        ("123", "1", True),
        ("UPPER", "U", True),
        ("lower", "L", False)
    ])
    def test_starts_with(self, utils, string, symbol, expected):
        assert utils.starts_with(string, symbol) == expected
    
    # Тесты для end_with
    @pytest.mark.parametrize("string, symbol, expected", [
        ("SkyPro", "o", True),
        ("SkyPro", "y", False),
        ("", "a", False),
        ("hello", "", True),  # Дефект: пустая строка всегда в конце
        ("test ", " ", True),
        ("123", "3", True),
        ("END", "D", True),
        ("end", "D", False)
    ])
    def test_end_with(self, utils, string, symbol, expected):
        assert utils.end_with(string, symbol) == expected
    
    # Тесты для is_empty
    @pytest.mark.parametrize("string, expected", [
        ("", True),
        (" ", True),
        ("SkyPro", False),
        ("  ", True),
        ("\t", False),  # Дефект: табы не считаются пробелами
        ("\n", False),  # Дефект: переносы не считаются пробелами
        (" a ", False),
        ("   ", True)
    ])
    def test_is_empty(self, utils, string, expected):
        assert utils.is_empty(string) == expected
    
    # Тесты для list_to_string
    @pytest.mark.parametrize("lst, joiner, expected", [
        ([1, 2, 3, 4], ", ", "1, 2, 3, 4"),
        (["Sky", "Pro"], ", ", "Sky, Pro"),
        (["Sky", "Pro"], "-", "Sky-Pro"),
        ([], ", ", ""),
        (["single"], ", ", "single"),
        ([1, 2, 3], "", "123"),  # Дефект: разделитель не применяется корректно
        (["a", "b", "c"], " - ", "a - b - c"),
        ([None, "test"], ", ", "None, test"),
        ([True, False], ", ", "True, False")
    ])
    def test_list_to_string(self, utils, lst, joiner, expected):
        assert utils.list_to_string(lst, joiner) == expected
    
    # Негативные тесты для list_to_string
    def test_list_to_string_default_joiner(self, utils):
        assert utils.list_to_string([1, 2, 3]) == "1, 2, 3"
    
    def test_list_to_string_single_element(self, utils):
        assert utils.list_to_string(["alone"]) == "alone"
    
    def test_list_to_string_none_elements(self, utils):
        assert utils.list_to_string([None, None]) == "None, None"