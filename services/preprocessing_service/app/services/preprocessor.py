import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


class Preprocessor:
    def process(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            raise ValueError("No raw data found for preprocessing")

        X = df[["sepal_length", "sepal_width", "petal_length", "petal_width"]].copy()
        y = df["species"].copy()

        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        train_df = pd.DataFrame(X_train_scaled, columns=X.columns)
        train_df["target"] = y_train
        train_df["dataset_type"] = "train"

        test_df = pd.DataFrame(X_test_scaled, columns=X.columns)
        test_df["target"] = y_test
        test_df["dataset_type"] = "test"

        processed_df = pd.concat([train_df, test_df], ignore_index=True)
        return processed_df