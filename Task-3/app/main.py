from fastapi import FastAPI
import psycopg2
from contextlib import contextmanager

app = FastAPI()

@contextmanager
def get_db():
    conn = psycopg2.connect("postgres://app_user:default_pg_pass@postgres:5432/app_db")
    try:
        yield conn
    finally:
        conn.close()

@app.get("/health")
def health():
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
    return {"status": "healthy", "db": "connected"}
