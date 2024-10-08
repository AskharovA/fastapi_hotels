FROM python:3.11.9-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD alembic upgrade head; python src/main.py
