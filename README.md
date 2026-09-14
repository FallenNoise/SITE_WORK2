# CryBloga - Блог на Django

Учебный проект блога, созданный на фреймворке Django. Реализован базовый CRUD-функционал (создание, чтение, обновление и удаление постов) с использованием встроенных форм (Forms / ModelForm).

## Стек технологий

- Python 3
- Django
- HTML / CSS
- SQLite (база данных по умолчанию)

## Инструкция по локальному запуску

1. Клонируйте репозиторий:
   ```bash
   git clone <ссылка_на_ваш_репозиторий>
   ```
2. python -m venv .venv
   source .venv/Scripts/activate # Для Windows

3. pip install -r requirements.txt

4. python manage.py migrate

5. python manage.py runserver
