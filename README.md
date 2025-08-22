# Инструкция по запуску проекта через docker-compose
1. Скопировать .env.example → .env и заполнить. 
2. docker compose up -d --build 
3. Проверки:
   * Web: открыть http://localhost:8001
   * Postgres: docker compose exec db psql -U $USER -d $NAME -c '\l'
   * Redis: docker compose exec redis redis-cli PING → PONG
   * Celery: docker compose logs -f celery
   * Beat: docker compose logs -f beat