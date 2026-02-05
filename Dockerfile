# 1. Базовый образ
FROM python:3.13-slim

# 2. Системные зависимости для asyncpg
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Рабочая директория — корень проекта
WORKDIR /app

# 4. Копируем зависимости
COPY requirements.txt /app/

# 5. Устанавливаем Python-зависимости
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# 6. Копируем весь проект (включая main.py и src/)
COPY . /app

# 7. Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

# 8. Запуск бота через main.py
CMD ["python", "main.py"]
