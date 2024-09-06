# Dockerfile - Speech Recognition Service

# Використовуємо офіційний Python образ як базовий
FROM python:3.9-slim

# Встановлюємо робочу директорію в контейнері
WORKDIR /vosk
RUN pip install --upgrade pip
# Встановлюємо PyTorch із зазначеного джерела
RUN pip install torch --extra-index-url https://download.pytorch.org/whl/torch_stable.html 
# Копіюємо requirements.txt і встановлюємо залежності
COPY requirements_vosk.txt ./
RUN pip install --no-cache-dir -r requirements_vosk.txt

COPY . .

EXPOSE 8002
