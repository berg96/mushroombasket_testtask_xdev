FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y build-essential

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY /app .

COPY alembic.ini .

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000