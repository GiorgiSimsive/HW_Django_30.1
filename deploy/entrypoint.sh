#!/usr/bin/env bash
set -e

python - <<'PY'
import os, time, psycopg2
from psycopg2 import OperationalError

host = os.getenv("DATABASE_HOST") or os.getenv("HOST") or "db"
name = os.getenv("POSTGRES_DB") or os.getenv("NAME")
user = os.getenv("POSTGRES_USER") or os.getenv("USER")
password = os.getenv("POSTGRES_PASSWORD") or os.getenv("PASSWORD")

print(f"Waiting for Postgres host={host} db={name} user={user}")

for i in range(120):  # 2 минуты на всякий
    try:
        psycopg2.connect(host=host, dbname=name, user=user, password=password).close()
        print("Postgres is ready")
        break
    except OperationalError as e:
        time.sleep(1)
else:
    raise SystemExit("Postgres is not ready")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec gunicorn myproject.wsgi:application -b 0.0.0.0:8000 --workers 3

