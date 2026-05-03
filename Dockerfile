FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY ./migrations ./migrations
COPY ./alembic.ini .
COPY ./docker/start.sh /start.sh

RUN chmod +x /start.sh && mkdir -p /app/data /app/logs

EXPOSE 8000

CMD ["/start.sh"]
