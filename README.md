# Проект "Хакатон Лента"

Проект "Хакатон Лента" - это разработка алгоритма и интерфейса предсказательной модели для сети магазинов "Лента". 

![DRF](https://www.django-rest-framework.org/img/logo.png)

## Авторы

- [Юрий Квасков](https://github.com/YuraKvaskov)
- [Олег Ильичевич](https://github.com/oitczvovich)

## Запуск в Docker

Для запуска проекта в Docker выполните следующие шаги:

1. Выполните команду для скачивания Docker-образа проекта:
```
docker pull yuraskv/lenta
```
2. Запустите контейнер с проектом:
```
docker run -p 8000:8000 yuraskv/lenta
```
## Запуск без Docker

Для запуска проекта без Docker, выполните следующие шаги:

1. Клонируйте проект:
git clone https://github.com/YuraKvaskov/your-project-name.git

2. Создайте виртуальное окружение:
python -m venv venv

3. Активируйте виртуальное окружение:

- На Windows:

  ```
  venv\Scripts\activate
  ```

- На macOS и Linux:

  ```
  source venv/bin/activate
  ```

4. Перейдите в папку проекта:
   ```
   cd lenta
   ```
   
5. Выполните миграции для базы данных:
   ```
   python manage.py makemigrations
   ```
   ```
   python manage.py migrate
   ```
   
6. Создайте суперпользователя:
   ```
   python manage.py createsuperuser
   ```
7. Запустите сервер:
   ```
   python manage.py runserver
   ```

Документация к проекту доступна по адресу:

[http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
