FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py train.py inspect_data.py ./
COPY templates ./templates
COPY static ./static
COPY models ./models

EXPOSE 5000

CMD ["python", "app.py"]
