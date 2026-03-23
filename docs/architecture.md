# 🏗️ System Architecture

---

## Overview

This project implements a microservices architecture for a complete ML pipeline.

---

## Architecture Diagram

```
          +------------------+
          |   Frontend       |
          |    Flask         |
          +--------+---------+
                   |
                   v
          +------------------+
          | Prediction API   |
          +--------+---------+
                   |
                   v
          +------------------+
          |   MLflow Model   |
          +--------+---------+
                   |
          +--------+---------+
          | Training Service |
          +--------+---------+
                   |
          +--------+---------+
          | Preprocessing    |
          +--------+---------+
                   |
          +--------+---------+
          | Ingestion        |
          +--------+---------+
                   |
          +------------------+
          | PostgreSQL DB    |
          +------------------+
```

---

## Services

### Ingestion Service

* CSV reading
* Data cleaning
* Storage

### Preprocessing Service

* Scaling
* Encoding
* Feature preparation

### Training Service

* Model training
* Evaluation
* MLflow logging

### Prediction Service

* Prediction
* Feedback loop

### Frontend

* UI
* Authentication
* User interaction

---

## Key Concepts

* Microservices architecture
* Separation of concerns
* Model lifecycle management
* Feedback-driven improvement
