# 🏗️ Архитектура и структура проекта

## 📋 Обзор архитектуры

**TasKanLine Backend** построен по принципам **Clean Architecture** с четким разделением слоев ответственности. Это обеспечивает масштабируемость, тестируемость и легкость поддержки кода.

### 🎯 Основные принципы

- **🔄 Dependency Injection** — все зависимости передаются через конструкторы
- **🗂️ Разделение ответственности** — каждый модуль выполняет свою задачу
- **⚡ Асинхронность** — все операции с БД выполняются асинхронно
- **🛡️ Типизация** — строгая типизация на всех уровнях
- **🔧 Конфигурируемость** — гибкая настройка окружения

## 📁 Структура проекта

### 📂 Основные каталоги и файлы

```
📁 TasKanLine/server/
├── 📁 src/                          # Основной исходный код
│   ├── 📁 api/                      # API роуты и контроллеры
│   │   ├── 📁 v1/                   # API версии 1
│   │   │   ├── 📄 auth.py          # Эндпоинты аутентификации
│   │   │   └── 📄 __init__.py      # Инициализация модуля
│   │   └── 📄 __init__.py          # Инициализация API
│   ├── 📁 core/                     # Основная конфигурация
│   │   ├── 📄 config.py            # Настройки приложения
│   │   ├── 📄 depends.py           # Зависимости FastAPI
│   │   └── 📄 security.py          # Настройка безопасности JWT
│   ├── 📁 crud/                     # Бизнес-логика работы с данными
│   │   ├── 📄 auth.py              # CRUD операции для пользователей
│   │   └── 📄 __init__.py          # Инициализация CRUD
│   ├── 📁 database/                 # Работа с базой данных
│   │   └── 📄 session.py           # Настройка SQLAlchemy сессий
│   ├── 📁 models/                   # SQLAlchemy модели данных
│   │   ├── 📄 users.py             # Модели User и UserProfile
│   │   └── 📄 __init__.py          # Инициализация моделей
│   ├── 📁 schemas/                  # Pydantic схемы валидации
│   │   ├── 📄 auth.py              # Схемы для аутентификации
│   │   └── 📄 __init__.py          # Инициализация схем
│   ├── 📁 services/                 # Сервисный слой (готов к расширению)
│   │   └── 📄 main.py              # Основные сервисы
│   └── 📄 main.py                   # Точка входа в приложение
├── 📁 docs/                         # Документация проекта
├── 📁 database/                     # Файлы баз данных (SQLite)
├── 📄 .env.example                  # Пример конфигурации окружения
├── 📄 .gitignore                    # Игнорируемые файлы Git
├── 📄 .python-version               # Версия Python для uv
├── 📄 Dockerfile                    # Инструкция сборки Docker образа
├── 📄 Makefile                      # Команды управления проектом
├── 📄 pyproject.toml               # Метаданные проекта и зависимости
├── 📄 requirements.txt             # Зависимости для Docker
├── 📄 README.md                     # Основная документация
└── 📄 uv.lock                      # Заблокированные зависимости uv
```

### 📝 Назначение основных файлов

| Файл | Назначение | Ключевая функциональность |
|------|------------|---------------------------|
| **`src/main.py`** | Точка входа | Создание FastAPI приложения, настройка middleware |
| **`src/core/config.py`** | Конфигурация | Настройки БД, JWT, CORS, переменные окружения |
| **`src/core/security.py`** | Безопасность | Настройка AuthX, JWT токены, куки |
| **`src/core/depends.py`** | Зависимости | Сессии БД, аутентификация пользователей |
| **`src/database/session.py`** | БД сессии | SQLAlchemy engine, сессии, подключение |
| **`src/models/users.py`** | Модели данных | User, UserProfile модели SQLAlchemy |
| **`src/schemas/auth.py`** | Схемы | Pydantic модели для валидации данных |
| **`src/crud/auth.py`** | Бизнес-логика | CRUD операции для пользователей |
| **`src/api/v1/auth.py`** | API роуты | Эндпоинты /signup, /login, /protected |

## 🎨 Визуализация архитектуры

### 📊 Интерактивная диаграмма репозитория

```mermaid
graph TB
    subgraph "📁 TasKanLine/server/"
        A[📄 README.md] --> B[📁 src/]
        A --> C[📁 docs/]
        A --> D[📄 Dockerfile]
        A --> E[📄 Makefile]
        A --> F[📄 pyproject.toml]
        
        subgraph "📁 src/"
            B --> G[📄 main.py]
            B --> H[📁 api/]
            B --> I[📁 core/]
            B --> J[📁 crud/]
            B --> K[📁 models/]
            B --> L[📁 schemas/]
            B --> M[📁 database/]
            B --> N[📁 services/]
            
            subgraph "📁 api/"
                H --> O[📁 v1/]
                O --> P[📄 auth.py]
            end
            
            subgraph "📁 core/"
                I --> Q[📄 config.py]
                I --> R[📄 depends.py]
                I --> S[📄 security.py]
            end
            
            subgraph "📁 crud/"
                J --> T[📄 auth.py]
            end
            
            subgraph "📁 models/"
                K --> U[📄 users.py]
            end
            
            subgraph "📁 schemas/"
                L --> V[📄 auth.py]
            end
            
            subgraph "📁 database/"
                M --> W[📄 session.py]
            end
            
            subgraph "📁 services/"
                N --> X[📄 main.py]
            end
        end
        
        subgraph "📁 docs/"
            C --> Y[📄 index.md]
            C --> Z[📄 architecture.md]
            C --> AA[📄 installation.md]
            C --> BB[📄 usage.md]
            C --> CC[📄 contributing.md]
        end
    end
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#fff3e0
    style E fill:#fff3e0
    style F fill:#fff3e0
```

### 🔄 Flow Diagram архитектуры приложения

```mermaid
flowchart TD
    A[🌐 HTTP Request] --> B[🚀 FastAPI Application]
    B --> C[🔧 Middleware Layer]
    C --> D[📍 API Router]
    D --> E[🔐 Authentication Check]
    E --> F{Authenticated?}
    
    F -->|Yes| G[👤 User Context]
    F -->|No| H[🚫 401 Unauthorized]
    
    G --> I[📋 Request Validation]
    I --> J[🔍 Pydantic Schema]
    J --> K[💼 Business Logic]
    K --> L[🗄️ Database Operations]
    
    L --> M[🔄 SQLAlchemy ORM]
    M --> N[📊 Database]
    N --> O[✅ Response Processing]
    O --> P[📤 HTTP Response]
    
    subgraph "🏗️ Core Components"
        Q[⚙️ Config]
        R[🔐 Security]
        S[📝 Dependencies]
        T[🗄️ Sessions]
    end
    
    subgraph "📊 Data Flow"
        U[📥 Request Data]
        V[🔄 Validation]
        W[💾 Storage]
        X[📤 Response Data]
    end
    
    B -.-> Q
    E -.-> R
    K -.-> S
    L -.-> T
    
    style A fill:#e3f2fd
    style P fill:#e8f5e8
    style H fill:#ffebee
    style N fill:#fff3e0
```

### 🎯 Архитектурные слои

```mermaid
graph LR
    subgraph "🎯 Presentation Layer"
        A[🌐 API Endpoints]
        B[📝 Request/Response]
    end
    
    subgraph "🔧 Business Logic Layer"
        C[💼 CRUD Operations]
        D[🔍 Validation]
        E[👤 User Management]
    end
    
    subgraph "🗄️ Data Access Layer"
        F[🔄 SQLAlchemy ORM]
        G[📊 Database Models]
        H[🔗 Sessions]
    end
    
    subgraph "⚙️ Infrastructure Layer"
        I[🗄️ PostgreSQL/SQLite]
        J[🔐 JWT Security]
        K[📝 Configuration]
    end
    
    A --> C
    B --> D
    C --> F
    D --> G
    E --> H
    F --> I
    G --> J
    H --> K
    
    style A fill:#e3f2fd
    style C fill:#f3e5f5
    style F fill:#e8f5e8
    style I fill:#fff3e0
```

## 🔄 Поток данных в приложении

### 📋 Типичный запрос аутентификации

```mermaid
sequenceDiagram
    participant C as 🌐 Client
    participant A as 🚀 FastAPI
    participant M as 🔧 Middleware
    participant R as 📍 Router
    participant V as 🔍 Validator
    participant B as 💼 CRUD
    participant D as 🗄️ Database
    
    C->>A: POST /api/v1/auth/login
    A->>M: CORS & Security Check
    M->>R: Route to auth endpoint
    R->>V: Validate request body
    V->>B: Call login CRUD operation
    B->>D: Check user credentials
    D-->>B: User data
    B->>B: Verify password (Argon2)
    B->>B: Generate JWT token
    B-->>R: Success with token
    R->>A: Set cookie with token
    A-->>C: 200 OK with auth cookie
```

## 🎨 Принципы проектирования

### 🏛️ SOLID принципы в проекте

1. **S - Single Responsibility**: Каждый класс выполняет одну задачу
2. **O - Open/Closed**: Готов к расширению без модификации
3. **L - Liskov Substitution**: Модели корректно наследуются
4. **I - Interface Segregation**: Четкое разделение интерфейсов
5. **D - Dependency Inversion**: Зависимости инжектируются

### 🔄 Паттерны проектирования

- **🏭 Repository Pattern** — CRUD операции инкапсулированы
- **🔧 Dependency Injection** — зависимости передаются через FastAPI
- **🎭 Factory Pattern** — сессии БД создаются через фабрики
- **📝 Strategy Pattern** — разные БД (PostgreSQL/SQLite)

## 🚀 Масштабирование и расширение

### 📈 Готовность к росту

Архитектура проекта готова к:

- **📊 Новым модулям** — задачи, проекты, команды
- **🔌 Микросервисам** — выделение отдельных сервисов
- **🗄️ Разным БД** — Redis, MongoDB, другие SQL
- **🌐 Load Balancing** — горизонтальное масштабирование
- **📦 Caching** — многоуровневое кеширование

### 🎯 Следующие шаги развития

1. **📋 Task Management** — CRUD для задач
2. **👥 Team Collaboration** — команды и роли
3. **📊 Analytics** — отчеты и статистика
4. **🔔 Notifications** — система уведомлений
5. **🌐 API v2** — следующая версия API

---

**💡 Совет:** Изучите диаграммы выше, чтобы лучше понять, как компоненты взаимодействуют друг с другом. Это поможет вам эффективно работать с проектом! 🚀