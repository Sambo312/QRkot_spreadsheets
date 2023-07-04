# QRKot

Проект QRKot приложение для Благотворительного фонда поддержки котиков.

Технологии:

```
Python 3.9, FastApi 0.78, Sqlalchemy 1.4, Alembic 1.7
```

***Чтобы развернуть проект необходимо:***

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:Sambo312/cat_charity_fund.git
```

```bash
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

Создать файл .env в котором определить переменные с именем приложения, средой выполнения, доступом к БД, а также значение для SECRET_KEY:

```
APP_TITLE=
APP_DESCRIPTION=
DATABASE_URL=
SECRET=
```

Инициировать `alembic`:

```bash
alembic init --template async alembic
```

Внести изменения в файлы конфигурации alembic: `alembic.ini`, `alembic/env.py`

Выполнить миграции:

```bash
alembic revision --autogenerate -m "First migration"
alembic upgrade head
```

Запуск проекта:

```bash
uvicorn app.main:app
```

**Автор проекта:** [Хомутов Евгений](https://github.com/Sambo312/)
