FROM python:3.10

WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY __init__.py .
COPY worker.py .

ENTRYPOINT celery -A worker worker --autoscale 10 --loglevel=info
