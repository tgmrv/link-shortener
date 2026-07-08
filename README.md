# Link Shortener

Сервис сокращения ссылок на FastAPI + PostgreSQL + Docker.

## Стек

- Python 3.14
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Docker

## API

POST /links — создать короткую ссылку

GET /links — список всех ссылок

GET /{short_code} — редирект

## Запуск

```bash
docker-compose up -d
uvicorn app.main:app --reload