# FastAPI + PostgreSQL + Docker

Проект запускается в двух контейнерах:
- `db` (PostgreSQL)
- `api` (FastAPI)

При старте `api` автоматически выполняются миграции Alembic.

## Запуск

```bash
docker compose up --build
```

## Что доступно после старта

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL в сети Docker: `db:5432`
