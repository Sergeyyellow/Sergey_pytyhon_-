
import pytest
from sqlalchemy import create_engine, Column, Integer, String, Boolean, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import event
from sqlalchemy.orm import Session

# === НАСТРОЙКИ ПОДКЛЮЧЕНИЯ ===
# ЗАМЕНИТЕ ЭТИ ПАРАМЕТРЫ НА ВАШИ РЕАЛЬНЫЕ!
DB_USER = "myuser"
DB_PASSWORD = "simplepassword123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mydatabase"

# Строка подключения как в задании
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()

# Модель для тестирования - используем другое имя таблицы
class Student(Base):
    __tablename__ = 'test_students_lesson9'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    is_active = Column(Boolean, default=True, server_default='true')  # Добавляем server_default
    
    def __init__(self, **kwargs):
        """Инициализатор с установкой дефолтных значений"""
        # Вызываем родительский инициализатор
        super().__init__(**kwargs)
        # Устанавливаем дефолтное значение is_active если оно не передано
        if 'is_active' not in kwargs:
            self.is_active = True
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"

# Фикстуры для pytest
@pytest.fixture(scope="function")
def engine():
    """Создает engine для подключения к БД"""
    engine = create_engine(DATABASE_URL)
    
    # Проверяем подключение
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✓ Подключение к БД успешно")
    except Exception as e:
        pytest.skip(f"Не удалось подключиться к БД: {e}")
    
    return engine

@pytest.fixture(scope="function")
def setup_tables(engine):
    """Создает таблицу только если её нет"""
    try:
        # Проверяем права на создание таблицы
        with engine.connect() as conn:
            # Пытаемся создать временную таблицу
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS test_students_lesson9 (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """))
            conn.commit()
            print("✓ Таблица создана или уже существует")
        
        yield
        
        # Очищаем таблицу после теста
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE test_students_lesson9 RESTART IDENTITY CASCADE"))
            conn.commit()
        
    except Exception as e:
        print(f"⚠ Ошибка при работе с таблицей: {e}")
        pytest.skip(f"Не удалось работать с таблицей: {e}")

@pytest.fixture
def db_session(engine, setup_tables):
    """Создает сессию для работы с БД"""
    connection = engine.connect()
    
    # Начинаем транзакцию
    trans = connection.begin()
    
    Session = sessionmaker(bind=connection)
    session = Session()
    
    # Очищаем таблицу перед тестом
    try:
        session.execute(text("TRUNCATE TABLE test_students_lesson9 RESTART IDENTITY CASCADE"))
        session.commit()
    except:
        session.rollback()
    
    yield session
    
    # Очистка после теста
    try:
        session.rollback()
    except:
        pass
    
    session.close()
    
    # Откатываем транзакцию
    try:
        trans.rollback()
    except:
        pass
    
    connection.close()