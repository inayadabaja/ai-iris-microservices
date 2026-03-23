import pandas as pd


class CSVReader:
    def read_csv(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)