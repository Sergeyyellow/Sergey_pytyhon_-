import pytest
import os
import sys

if __name__ == "__main__":
    # Добавляем текущую директорию в путь
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    pytest.main(["tests/"])