FROM python:3.11-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir


COPY . /app

WORKDIR /app

EXPOSE 8000

CMD ["gunicorn", "lenta.wsgi:application", "--bind", "0:8000" ] 