FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir mlflow psycopg2-binary

EXPOSE 5000

CMD ["mlflow", "server", \
     "--host", "0.0.0.0", \
     "--port", "5000", \
     "--backend-store-uri", "sqlite:///app/mlflow_data/mlflow.db", \
     "--default-artifact-root", "/app/mlruns", \
     "--serve-artifacts"]