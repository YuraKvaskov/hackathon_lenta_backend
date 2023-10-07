FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

ENV PIP_ROOT_USER_ACTION=ignore

COPY . /app

WORKDIR /app

# Создание миграций
RUN python3 manage.py makemigrations

# Применение миграций
RUN python3 manage.py migrate

# Создание суперпользователя (если необходимо)
# RUN python3 manage.py createsuperuser --username admin --email admin@example.com

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0:8000"]

