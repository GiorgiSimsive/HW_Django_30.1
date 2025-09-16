# Инструкция по запуску проекта через docker-compose
1. Скопировать .env.example → .env и заполнить. 
2. docker compose up -d --build 
3. Проверки:
   * Web: открыть http://localhost:8001
   * Postgres: docker compose exec db psql -U $USER -d $NAME -c '\l'
   * Redis: docker compose exec redis redis-cli PING → PONG
   * Celery: docker compose logs -f celery
   * Beat: docker compose logs -f beat
# Django Project – CI/CD + Deploy on Yandex Cloud

## 📌 Описание
Учебный проект на Django с настроенным CI/CD пайплайном через **GitHub Actions** и автоматическим деплоем на удалённый сервер в **Yandex Cloud**.

---

## ⚙️ Настройка удалённого сервера

### 1. Создание виртуальной машины
1. Перейдите в [Yandex Cloud Console](https://console.cloud.yandex.ru/).
2. Создайте ВМ в сервисе **Compute Cloud**:
   - Образ: `Ubuntu 22.04 LTS`
   - Пользователь: `ubuntu`
   - Подключите свой SSH-ключ при создании.
3. Убедитесь, что ВМ получила публичный IPv4.

### 2. Настройка сети и firewall
1. В разделе **VPC → Security Groups** создайте группу правил.
2. Разрешите входящие соединения:
   - `TCP 22` — SSH-доступ
   - `TCP 80` — HTTP
   - `TCP 443` — HTTPS
3. Привяжите security group к вашей ВМ.

### 3. Установка зависимостей на сервере
Подключитесь к серверу:
```bash
ssh -i ~/.ssh/id_ed25519 ubuntu@<SERVER_IP>
