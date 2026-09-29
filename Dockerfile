# 1. Базовый образ (легковесный Python)
FROM python:3.11-slim

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл с зависимостями (пока нет, но создадим)
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем всё приложение
COPY . .

# 6. Открываем порт 8000
EXPOSE 8000

# 7. Команда запуска
CMD ["python", "app.py"]
