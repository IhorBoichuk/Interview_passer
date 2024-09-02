FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    build-essential \
    ffmpeg \
    tk \
    xvfb \
    && rm -rf /var/lib/apt/lists/*



RUN pip install --upgrade pip

COPY requirements_rec.txt .

RUN pip install --no-cache-dir -r requirements_rec.txt

COPY . /app

WORKDIR /app

EXPOSE 5000

ENV PYTHONPATH=/

CMD ["python","-m", "main"]
