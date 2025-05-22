# Foodgram - Помощник в приготовлении вкусных блюд 😋

## Запуск проекта

### Требования
- Docker
- Docker Compose

### 1. Клонирование репозитория
```bash
git clone https://github.com/alexaaa-a/foodgram-st.git
cd foodgram-st
```

### 2. Настройка окружения
Создайте файлы с переменными окружения:
```bash
# .env
POSTGRES_USER=postgres
POSTGRES_DB=foodgram
POSTGRES_PASSWORD=12345
DB_PORT=5432
DB_HOST=db
```

### 3. Запуск контейнеров
```bash
docker-compose up --build
```
