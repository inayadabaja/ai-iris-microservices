# 🚀 Deployment Guide

---

## Prerequisites

* Docker
* Docker Compose

---

## Run the Project

```bash
docker compose up --build
```

---

## Services Startup Order

1. PostgreSQL
2. Ingestion
3. Preprocessing
4. Training
5. Prediction
6. Frontend

---

## Environment Variables

Defined in `.env`:

```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=iris_db
```

---

## Access Services

* Frontend: http://localhost:5001
* MLflow: http://localhost:5000

---

## Logs

```bash
docker compose logs -f
```

---

## Stop

```bash
docker compose down
```

---

## Troubleshooting

### Database not reachable

```bash
docker ps
```

### Port conflict

* Change ports in docker-compose

---

## Production Improvements

* Add Nginx reverse proxy
* Add monitoring
* Enable HTTPS
