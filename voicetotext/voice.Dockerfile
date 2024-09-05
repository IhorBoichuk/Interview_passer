# Dockerfile - Speech Recognition Service

# Використовуємо офіційний Python образ як базовий
FROM python:3.9-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /vosk

# Копіюємо requirements.txt і встановлюємо залежності
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8002
