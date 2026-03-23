# 🚀 AI Iris Microservices

End-to-end MLOps system built using a microservices architecture with FastAPI, Flask, MLflow, PostgreSQL, and Docker.

---

## 🧠 Project Overview

This project demonstrates a complete machine learning pipeline deployed as independent microservices:

* Data ingestion from CSV
* Data preprocessing and transformation
* Model training and evaluation
* Model tracking with MLflow
* Prediction API with feedback loop
* Web interface for interaction
* Fully containerized system with Docker
* CI/CD pipeline with GitHub Actions

---

## 🏗️ Architecture

```
Frontend (Flask)
        ↓
Prediction API
        ↓
MLflow Model
        ↑
Training API
        ↑
Preprocessing API
        ↑
Ingestion API → PostgreSQL
```

---

## 🧪 Machine Learning Pipeline

1. **Ingestion Service**

   * Reads Iris CSV
   * Cleans data
   * Stores in raw database

2. **Preprocessing Service**

   * Encodes labels
   * Scales features
   * Stores processed dataset

3. **Training Service**

   * Trains ML model
   * Evaluates performance
   * Logs model in MLflow

4. **Prediction Service**

   * Loads trained model
   * Returns predictions
   * Stores predictions
   * Collects user feedback

---

## 🧰 Tech Stack

* FastAPI
* Flask
* PostgreSQL
* MLflow
* Docker
* Pytest
* GitHub Actions

---

## 🚀 Run the Project

```bash
docker compose up --build
```

---

## 🌐 Services

* Frontend: http://localhost:5001
* Ingestion API: http://localhost:8001/docs
* Preprocessing API: http://localhost:8002/docs
* Training API: http://localhost:8003/docs
* Prediction API: http://localhost:8004/docs
* MLflow UI: http://localhost:5000

---

## 🧪 Run Tests

```bash
pytest
```

---

## 🔁 Feedback Loop

Users can validate predictions using:

* 👍 True prediction
* 👎 False prediction

This enables future model retraining.

---

## 📦 Project Structure

```
ai_iris_microservices/
├── services/
├── frontend_flask/
├── shared/
├── databases/
├── mlruns/
├── scripts/
└── docs/
```

---

## 👨‍💻 Author

**Inaya Dabaja**
