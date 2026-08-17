# Advertisement Marketplace API
Асинхронный REST API сервис для публикации и поиска объявлений, реализованный на FastAPI, SQLAlchemy (Async) и PostgreSQL.

## 🛠 Стек технологий
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- asyncpg
- Pydantic
- Uvicorn

## 📁 Структура проекта
```
Plaintext
├── app/
│   ├── app.py          # Основное приложение FastAPI и роуты
│   ├── config.py       # Загрузка и управление конфигурацией (.env)
│   ├── database.py     # Инициализация async engine и фабрики сессий
│   ├── dependencies.py # Зависимости FastAPI
│   ├── lifespan.py     # Управление жизненным циклом (создание таблиц при старте)
│   ├── models.py       # ORM-модели базы данных (SQLAlchemy)
│   ├── schemas.py      # Схемы валидации и сериализации (Pydantic)
│   └── services.py     # Бизнес-логика и операции с БД (CRUD)
├── .env.example        # Пример переменных окружения
├── requirements.txt    # Зависимости проекта
└── README.md
```
## 🚀 Установка и запуск
1. Клонирование репозитория
```Bash
git clone <URL_РЕПОЗИТОРИЯ>
cd <ПАПКА_ПРОЕКТА>
```
2. Настройка виртуального окружения
```Bash
python -m venv venv
# source venv/bin/activate  # Linux/macOS
venv\Scripts\activate   # Windows
pip install -r requirements.txt
```
3. Настройка переменных окружения
Создайте файл .env в корневой директории:
```
Фрагмент кода
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=marketplace_db
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

## Основные endpoints

| Метод  | Endpoint                | Назначение                    |
|--------|-------------------------|-------------------------------|
| POST   | `/advertisement`        | Создать объявление             |
| GET    | `/advertisement/{id}`   | Получить объявление по ID      |
| PATCH  | `/advertisement/{id}`   | Обновить объявление            |
| DELETE | `/advertisement/{id}`   | Удалить объявление             |
| GET    | `/advertisement`        | Получить и искать объявления   |


Поиск по заголовку:

```text
GET /advertisement?title=iphone
```
Поиск по описанию:
```text
GET /advertisement?description=gaming
```
Фильтрация по диапазону цены:
```text
GET /advertisement?min_price=10000&max_price=50000
```
Комбинированный поиск:
```text
GET /advertisement?title=iphone&max_price=50000
```