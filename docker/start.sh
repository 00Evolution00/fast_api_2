#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
until alembic upgrade head; do
  echo "Database is unavailable, retrying in 2 seconds..."
  sleep 2
done

exec uvicorn src.main:app --host 0.0.0.0 --port 8000
