# Лаба PostgreSQL локально через Docker

## Что внутри
- `docker-compose.yml` — поднимает локальный PostgreSQL в Docker;
- `docker/db/Dockerfile` — скачивает и встраивает demo-базу «Авиаперевозки»;
- `Task_3_Postgre_local_docker.ipynb` — готовый ноутбук с решениями;
- `lab_solution.py` — запуск тех же запросов как обычного Python-скрипта.

## 1. Что установить
- Docker Desktop
- Python 3.11+
- Visual Studio Code с расширениями **Python** и **Jupyter**

## 2. Как запустить базу
В корне проекта выполни:

```bash
docker compose up --build -d
```

Проверь, что контейнер стал `healthy`:

```bash
docker ps
```

Если база поднимается первый раз, инициализация может занять несколько минут, потому что образ скачивает demo-базу и импортирует её.

## 3. Подготовь Python-окружение
```bash
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### Установка библиотек
```bash
pip install -r requirements.txt
```

## 4. Создай `.env`
Скопируй `.env.example` в `.env`.

Готовые значения уже подходят для Docker:

```env
POSTGRESQL_HOST=localhost
POSTGRESQL_PORT=5433
POSTGRESQL_DB=demo
POSTGRESQL_USER=demo
POSTGRESQL_PASSWORD=demo
```

## 5. Запуск в VS Code
1. Открой папку проекта.
2. Открой `Task_3_Postgre_local_docker.ipynb`.
3. Выбери kernel из `.venv`.
4. Нажми **Run All**.

## 6. Запуск без ноутбука
```bash
python lab_solution.py
```

## 7. Как остановить базу
```bash
docker compose down
```

Если хочешь удалить и данные тоже:

```bash
docker compose down -v
```

## 8. Частые проблемы
### Порт занят
Если `5433` уже занят, поменяй строку в `docker-compose.yml`:
```yaml
ports:
  - "5434:5432"
```
Тогда и в `.env` укажи:
```env
POSTGRESQL_PORT=5434
```

### База не импортировалась
Сбрось volume и пересобери:
```bash
docker compose down -v
docker compose up --build -d
```

### Не подключается ноутбук
Проверь:
- контейнер запущен;
- в `.env` совпадают host/port/user/password;
- выбран правильный Python kernel.
