"""
Тесты для CRUD операций
Соответствует требованиям задания:
- 3 теста: добавление, изменение, удаление
- Использует pytest и SQLAlchemy
- Тесты стабильны и удаляют за собой данные
"""
import pytest
from sqlalchemy import text, exc
from conftest import Student

def test_create_student(db_session):
    """Тест на добавление записи (CREATE)"""
    print("\n=== Тест CREATE ===")
    
    # Arrange
    new_student = Student(
        name="John Doe",
        email="john.doe@example.com"
    )
    
    # Проверяем что is_active установлен по умолчанию
    assert new_student.is_active == True
    
    # Act
    db_session.add(new_student)
    db_session.commit()
    
    # Assert
    saved_student = db_session.query(Student).filter_by(
        email="john.doe@example.com"
    ).first()
    
    assert saved_student is not None
    assert saved_student.name == "John Doe"
    assert saved_student.email == "john.doe@example.com"
    assert saved_student.is_active == True
    
    print(f"✓ Создан студент: {saved_student.name} (ID: {saved_student.id})")

def test_update_student(db_session):
    """Тест на изменение записи (UPDATE)"""
    print("\n=== Тест UPDATE ===")
    
    # Arrange - создаем запись
    student = Student(
        name="Alice Smith",
        email="alice@example.com"
    )
    db_session.add(student)
    db_session.commit()
    
    # Act - изменяем данные
    student_to_update = db_session.query(Student).filter_by(
        email="alice@example.com"
    ).first()
    
    assert student_to_update is not None
    student_to_update.name = "Alice Johnson"
    student_to_update.is_active = False  # Мягкое удаление
    db_session.commit()
    
    # Assert - проверяем изменения
    updated_student = db_session.query(Student).filter_by(
        email="alice@example.com"
    ).first()
    
    assert updated_student is not None
    assert updated_student.name == "Alice Johnson"
    assert updated_student.is_active == False
    
    print(f"✓ Обновлен студент: {updated_student.name} (активен: {updated_student.is_active})")

def test_delete_student(db_session):
    """Тест на удаление записи (DELETE)"""
    print("\n=== Тест DELETE ===")
    
    # Arrange - создаем запись
    student = Student(
        name="Bob Brown",
        email="bob@example.com"
    )
    db_session.add(student)
    db_session.commit()
    
    # Проверяем, что запись создана
    created_student = db_session.query(Student).filter_by(
        email="bob@example.com"
    ).first()
    assert created_student is not None
    
    # Act - удаляем запись
    db_session.delete(created_student)
    db_session.commit()
    
    # Assert - проверяем удаление
    deleted_student = db_session.query(Student).filter_by(
        email="bob@example.com"
    ).first()
    assert deleted_student is None
    
    print("✓ Студент успешно удален")

def test_soft_delete_student(db_session):
    """Дополнительный тест на мягкое удаление (по статье из задания)"""
    print("\n=== Тест SOFT DELETE ===")
    
    # Arrange - создаем студента
    student = Student(
        name="Soft Delete Test",
        email="softdelete@example.com"
    )
    db_session.add(student)
    db_session.commit()
    
    # Act - выполняем мягкое удаление
    student_to_soft_delete = db_session.query(Student).filter_by(
        email="softdelete@example.com"
    ).first()
    student_to_soft_delete.is_active = False
    db_session.commit()
    
    # Assert - проверяем мягкое удаление
    soft_deleted = db_session.query(Student).filter_by(
        email="softdelete@example.com"
    ).first()
    assert soft_deleted is not None
    assert soft_deleted.is_active == False
    
    # Проверяем, что в активных студентах его нет
    active_students = db_session.query(Student).filter_by(
        is_active=True
    ).all()
    student_emails = [s.email for s in active_students]
    assert "softdelete@example.com" not in student_emails
    
    print(f"✓ Мягкое удаление: {len(active_students)} активных студентов")

def test_database_connection(db_session):
    """Тест подключения к БД"""
    print("\n=== Тест подключения к БД ===")
    result = db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1
    print("✓ Подключение к БД работает")

def test_unique_email_constraint(db_session):
    """Тест уникальности email"""
    print("\n=== Тест UNIQUE constraint ===")
    
    # Создаем первого студента
    student1 = Student(
        name="First Student",
        email="unique@example.com"
    )
    db_session.add(student1)
    db_session.commit()
    
    # Пытаемся создать второго студента с тем же email
    student2 = Student(
        name="Second Student",
        email="unique@example.com"
    )
    db_session.add(student2)
    
    # Должна быть ошибка уникальности
    try:
        db_session.commit()
        assert False, "Ожидалась ошибка UNIQUE constraint"
    except exc.IntegrityError as e:
        # Проверяем что это ошибка уникальности
        assert 'unique' in str(e).lower() or 'duplicate' in str(e).lower()
        db_session.rollback()
        print("✓ UNIQUE constraint работает корректно")
    except Exception as e:
        db_session.rollback()
        raise