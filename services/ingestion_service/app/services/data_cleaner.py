import pandas as pd


class DataCleaner:
    REQUIRED_COLUMNS = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species"
    ]

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        df.columns = df.columns.str.strip().str.lower()

        df = df.rename(columns={
            "sepallengthcm": "sepal_length",
            "sepalwidthcm": "sepal_width",
            "petallengthcm": "petal_length",
            "petalwidthcm": "petal_width"
        })

        if "id" in df.columns:
            df = df.drop(columns=["id"])

        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise KeyError(", ".join(missing_columns))

        df = df.drop_duplicates()

        numeric_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
        for col in numeric_columns:
            df[col] = df[col].fillna(df[col].mean())

        df["species"] = df["species"].astype(str).str.strip().str.lower()
        df["species"] = df["species"].fillna(df["species"].mode()[0])

        return df