# TasKanLine Backend

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.122+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

Асинхронный REST API для системы управления задачами в стиле Kanban. Поддерживает регистрацию и аутентификацию пользователей, управление проектами, досками, колонками и задачами.

## Технологии

| Категория        | Технология     | Версия   |
|------------------|----------------|----------|
| Язык             | Python         | 3.13     |
| Фреймворк        | FastAPI        | 0.122+   |
| ORM              | SQLAlchemy     | 2.0+     |
| База данных      | PostgreSQL     | 15+      |
| Асинхронный драйвер | asyncpg     | 0.31+    |
| Аутентификация   | AuthX          | 1.4+     |
| Хеширование      | Argon2-cffi    | 25.1+    |
| ASGI сервер      | Uvicorn        | 0.38+    |
| Валидация        | Pydantic       | 2.12+    |
| Миграции         | Alembic        | 1.18+    |
| Линтер           | Ruff           | 0.14+    |

## Требования

- Python 3.13+
- PostgreSQL 15+ (запущенный и доступный)
- [uv](https://github.com/astral-sh/uv) — для локальной разработки
- Docker — для контейнерного запуска

## Установка

### Локальная разработка

```bash
# 1. Клонировать репозиторий
git clone <repository-url>
cd TasKanLine/server

# 2. Создать файл переменных окружения
cp .env.example .env
# Отредактировать .env — указать реквизиты PostgreSQL и JWT-секрет

# 3. Установить зависимости и запустить (hot reload)
make dev

# 4. Применить миграции (в отдельном терминале)
uv run alembic upgrade head
```

### Docker

```bash
# Сборка образа и запуск контейнера
make build-run

# Управление контейнером
make start    # запустить остановленный контейнер
make stop     # остановить контейнер
make clean    # удалить контейнер и образ

# Полное обновление (git pull + пересборка + запуск)
make update-app
```

## Переменные окружения

Создайте файл `.env` на основе `.env.example`:

| Переменная             | Описание                             | Обязательная | По умолчанию |
|------------------------|--------------------------------------|:------------:|:------------:|
| `CORE__HOST`           | Хост для запуска сервера             | ✅           | `0.0.0.0`    |
| `CORE__PORT`           | Порт для запуска сервера             | ✅           | `8000`       |
| `CORE__ALLOWED_ORIGINS`| Разрешённые CORS-источники (JSON)    | ✅           | `["*"]`      |
| `CORE__JWT_SECRET_KEY` | Секретный ключ для подписи JWT       | ✅           | —            |
| `DB__HOST`             | Хост PostgreSQL                      | ✅           | `localhost`  |
| `DB__PORT`             | Порт PostgreSQL                      | ✅           | `5432`       |
| `DB__USER`             | Пользователь PostgreSQL              | ✅           | `postgres`   |
| `DB__PASSWORD`         | Пароль PostgreSQL                    | ✅           | —            |
| `DB__DATABASE`         | Имя базы данных                      | ✅           | `postgres`   |

## Использование

После запуска сервер доступен по адресу `http://localhost:8000`.

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API

Базовый префикс всех эндпоинтов: `/api/v1`

### Аутентификация

| Метод  | Путь                  | Описание                          | Auth |
|--------|-----------------------|-----------------------------------|:----:|
| POST   | `/auth/signup`        | Регистрация нового пользователя   | —    |
| POST   | `/auth/login`         | Вход, устанавливает cookie с JWT  | —    |
| GET    | `/auth/me`            | Данные текущего пользователя      | ✅   |
| POST   | `/auth/logout`        | Выход, удаляет cookie             | —    |

### Проекты

| Метод  | Путь                  | Описание                          | Auth |
|--------|-----------------------|-----------------------------------|:----:|
| POST   | `/projects`           | Создать проект                    | ✅   |
| GET    | `/projects`           | Список своих проектов             | ✅   |
| GET    | `/projects/{id}`      | Получить проект по ID             | ✅   |
| DELETE | `/projects/{id}`      | Удалить проект                    | ✅   |

### Доски

| Метод  | Путь                              | Описание                     | Auth |
|--------|-----------------------------------|------------------------------|:----:|
| POST   | `/projects/{id}/boards`           | Создать доску в проекте      | ✅   |
| GET    | `/projects/{id}/boards`           | Список досок проекта         | ✅   |
| GET    | `/boards/{id}`                    | Получить доску по ID         | ✅   |
| DELETE | `/boards/{id}`                    | Удалить доску                | ✅   |

### Колонки

| Метод  | Путь                              | Описание                     | Auth |
|--------|-----------------------------------|------------------------------|:----:|
| POST   | `/boards/{id}/columns`            | Создать колонку в доске      | ✅   |
| GET    | `/boards/{id}/columns`            | Список колонок доски         | ✅   |
| DELETE | `/columns/{id}`                   | Удалить колонку              | ✅   |

### Задачи

| Метод  | Путь                              | Описание                     | Auth |
|--------|-----------------------------------|------------------------------|:----:|
| POST   | `/columns/{id}/tasks`             | Создать задачу в колонке     | ✅   |
| GET    | `/columns/{id}/tasks`             | Список задач колонки         | ✅   |
| GET    | `/tasks/{id}`                     | Получить задачу по ID        | ✅   |
| PATCH  | `/tasks/{id}`                     | Обновить задачу              | ✅   |
| PATCH  | `/tasks/{id}/move`                | Переместить задачу           | ✅   |
| DELETE | `/tasks/{id}`                     | Удалить задачу               | ✅   |

Аутентификация — JWT-токен, передаётся как cookie `access_token` или в заголовке `Authorization: Bearer <token>`.

## Структура проекта

```
.
├── src/
│   ├── main.py              # Точка входа, настройка FastAPI и CORS
│   ├── api/
│   │   ├── __init__.py      # Регистрация роутеров с префиксом /api
│   │   └── v1/
│   │       ├── __init__.py  # Сборка роутеров v1
│   │       ├── auth.py      # Эндпоинты аутентификации
│   │       ├── projects.py  # Эндпоинты проектов
│   │       ├── boards.py    # Эндпоинты досок
│   │       ├── columns.py   # Эндпоинты колонок
│   │       └── tasks.py     # Эндпоинты задач
│   ├── core/
│   │   ├── config.py        # Pydantic-настройки из переменных окружения
│   │   ├── database.py      # SQLAlchemy engine и Base
│   │   ├── depends.py       # FastAPI зависимости (сессия БД, JWT)
│   │   └── security.py      # Конфигурация AuthX
│   ├── crud/
│   │   ├── auth.py          # CRUD операции с пользователями
│   │   └── tasks.py         # CRUD операции с проектами, досками, колонками, задачами
│   ├── models/
│   │   ├── users.py         # ORM модели User, UserProfile
│   │   └── tasks.py         # ORM модели Project, Board, Column, Task
│   └── schemas/
│       ├── auth.py          # Pydantic схемы для аутентификации
│       └── tasks.py         # Pydantic схемы для задач
├── migrations/
│   ├── env.py               # Конфигурация Alembic
│   └── versions/            # Файлы миграций
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt         # Для Docker-сборки (генерируется через uv pip freeze)
├── alembic.ini
└── .env.example
```

## Миграции базы данных

```bash
# Создать новую миграцию
uv run alembic revision --autogenerate -m "описание изменений"

# Применить миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1
```

## Лицензия

Не указана.
