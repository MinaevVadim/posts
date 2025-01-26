# Сервис постов

Реализовать бэкенд сервиса постов.

1. Пользователь может добавить, посмотреть, удалить, редактировать пост.
2. Пользователь может оставить комментарий к посту 
3. Пост содержит картинку.
4. Пользователь может посмотреть, изменить, удалить комментарий
5. Пользователь может зафоловить, удалить другого пользователя.

### Используемые инструменты

* FastApi
* Python 3
* Redis
* RabbitMQ
* Prometheus, Grafana
* Pytest
* Factory-Boy
* Auth JWT
* Postgres
* SQLAlchemy
* Alembic
* Pydantic
* Nginx
* Docker, Docker-compose

### Установка

Чтобы запустить приложение, выполните следующую команду
```
docker compose up -d
```
И так же в оболочке shell внутри Docker для создания таблиц с помощью Alembic следующую команду:
```
Alembic revision --message="create tables" --autogenerate
```
Затем:
```
Alembic upgrade head
```