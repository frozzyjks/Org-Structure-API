# Org Structure API
REST API для управления организационной структурой: подразделения и сотрудники.
Поддерживает древовидную иерархию отделов.
---

## Стек технологий

- Python 3.11
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- SQLite (для тестов)
- Pytest + pytest-asyncio
- Docker + docker-compose
---

## Запуск проекта

### Клонирование
``` env
git clone <repo_url>
cd org_structure_api
```

### Запуск через Docker

```bash
docker-compose up --build
```

API будет доступен:
```bash
http://localhost:8000
```

Swagger UI:
```bash
http://localhost:8000/docs
```
---

## База данных
По умолчанию используется PostgreSQL (docker).

В тестах используется SQLite in-memory.

---

## Основной функционал

### Departments

Создать отдел
```bash
POST /departments/
```
```bash
{
  "name": "IT",
  "parent_id": null
}
```

---

### Получить дерево подразделений
```bash
GET /departments/{department_id}/tree
```

Возвращает вложенную структуру:
```bash
{
  "id": 1,
  "name": "Root",
  "children": [
    {
      "id": 2,
      "name": "Child",
      "children": []
    }
  ]
}
```

---

### Ограничения

- Имя отдела должно быть уникальным в рамках одного родителя
- Поддерживается вложенность подразделений

Проверка уникальности реализована:

- на уровне бизнес-логики (service)
- на уровне БД

---

## Тестирование

Запуск тестов:

```bash
docker-compose exec app pytest -v
```

Покрыто:

- создание отдела
- проверка уникальности имени
- построение дерева

---

## Архитектурные решения

- Асинхронная работа с БД
- Разделение слоев (repository/service)
- Переопределение dependency для тестов
- Изоляция тестовой БД
- Обработка IntegrityError
- Проверка бизнес-ограничений в service