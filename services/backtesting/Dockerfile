FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY src ./src
COPY services/backtesting ./services/backtesting
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "services.backtesting.main"]
