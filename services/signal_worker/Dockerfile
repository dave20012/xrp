FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY services/signal_worker ./services/signal_worker
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "services.signal_worker.main"]
