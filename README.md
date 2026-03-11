# FastAPI Backend with SQLite

This is a FastAPI backend application configured to use SQLite database.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run database migrations:
```bash
alembic upgrade head
```

3. Start the application:
```bash
uvicorn src.main:app --reload
```

## Environment Variables

You can customize the SQLite database path by setting `SQLITE_DB_PATH` in your `.env` file:

```
SQLITE_DB_PATH=app.db
```

## Database

The application uses SQLite as the database backend. The database file will be created automatically when you run the migrations for the first time.
