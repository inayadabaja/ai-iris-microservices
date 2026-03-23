import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session


class TrainingDataRepository:
    def fetch_processed_data(self, db: Session) -> pd.DataFrame:
        query = text("""
            SELECT sepal_length, sepal_width, petal_length, petal_width, target, dataset_type
            FROM processed_iris_data
        """)
        result = db.execute(query)
        rows = result.fetchall()

        if not rows:
            return pd.DataFrame(columns=[
                "sepal_length", "sepal_width", "petal_length", "petal_width", "target", "dataset_type"
            ])

        return pd.DataFrame(rows, columns=result.keys())