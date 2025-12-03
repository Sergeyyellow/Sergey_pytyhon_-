"""
Тесты для моделей SQLAlchemy
"""
import pytest
from conftest import Student

def test_student_creation():
    """Тест создания объекта модели"""
    # Тест 1: Создание без указания is_active
    student1 = Student(
        name="Test Student 1",
        email="test1@example.com"
    )
    
    assert student1.name == "Test Student 1"
    assert student1.email == "test1@example.com"
    assert student1.is_active == True  # Должно быть True по умолчанию
    
    # Тест 2: Создание с явным указанием is_active=False
    student2 = Student(
        name="Test Student 2",
        email="test2@example.com",
        is_active=False
    )
    
    assert student2.name == "Test Student 2"
    assert student2.email == "test2@example.com"
    assert student2.is_active == False
    
    print("✓ Тест создания модели пройден")

def test_student_repr():
    """Тест строкового представления"""
    student = Student(
        id=1,
        name="Test Student",
        email="test@example.com"
    )
    
    repr_str = repr(student)
    assert "Student" in repr_str
    assert "id=1" in repr_str
    assert "name='Test Student'" in repr_str
    
    print("✓ Тест repr пройден")

def test_student_without_email(db_session):
    """Тест валидации модели (должна быть ошибка при отсутствии email)"""
    # Создаем студента без email
    student = Student(name="No Email")
    
    # Добавляем в сессию
    db_session.add(student)
    
    # Должна быть ошибка при коммите (из-за NOT NULL constraint)
    try:
        db_session.commit()
        # Если дошли сюда, значит ошибки не было - это неверно
        assert False, "Ожидалась ошибка NOT NULL constraint"
    except Exception as e:
        # Проверяем что это ошибка связанная с NOT NULL
        error_msg = str(e).lower()
        assert 'not null' in error_msg or 'null value' in error_msg
    
    # Откатываем
    db_session.rollback()
    
    print("✓ Тест валидации пройден")