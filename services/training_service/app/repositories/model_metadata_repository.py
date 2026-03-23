class ModelMetadataRepository:
    def __init__(self):
        self.latest_training_result = None

    def save_latest_result(self, result: dict) -> None:
        self.latest_training_result = result

    def get_latest_result(self) -> dict | None:
        return self.latest_training_result