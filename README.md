# Link Shortener

Сервис сокращения ссылок на FastAPI + PostgreSQL.

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
# Скопировать репозиторий
git clone https://github.com/tgmrv/link-shortener.git
cd link-shortener

# Создать образы и запустить контейнеры сервис
docker-compose up -d --build

# Остановить сервис
docker-compose down

# Остановить сервис и удалить все данные
docker-compose down -v

# Удалить образ
docker rmi <имя_или_id>

# Узнать имена образов
docker images
