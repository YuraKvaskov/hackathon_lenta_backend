FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

ENV PIP_ROOT_USER_ACTION=ignore

COPY . /app

WORKDIR /app

EXPOSE 8000

RUN python3 manage.py makemigrations && \
    python3 manage.py migrate && \
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('user', 'user@example.com', 'password')" | python3 manage.py shell && \
    python manage.py my_commands

CMD ["python3", "manage.py", "runserver", "0:8000"]