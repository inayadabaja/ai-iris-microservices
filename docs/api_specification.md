# 📡 API Specification

---

## 🧪 Ingestion Service

### POST /ingest

Load CSV data into raw database.

**Response**

```json
{
  "message": "Data ingested successfully",
  "rows_inserted": 150
}
```

---

## 🔄 Preprocessing Service

### POST /preprocess

Process raw data into training-ready format.

**Response**

```json
{
  "message": "Data preprocessed successfully",
  "rows_inserted": 150
}
```

---

## 🧠 Training Service

### POST /train

Train ML model and log it in MLflow.

**Response**

```json
{
  "message": "Model trained successfully",
  "accuracy": 0.96
}
```

---

### GET /metrics/latest

```json
{
  "accuracy": 0.96,
  "precision": 0.95,
  "recall": 0.96
}
```

---

### GET /model/info

```json
{
  "model_name": "iris_classifier",
  "version": 1
}
```

---

## 🔮 Prediction Service

### POST /predict

**Request**

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response**

```json
{
  "prediction_id": 1,
  "predicted_class": "setosa"
}
```

---

### POST /feedback

```json
{
  "prediction_id": 1,
  "is_correct": true,
  "true_label": "setosa"
}
```
