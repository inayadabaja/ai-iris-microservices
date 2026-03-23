from pydantic import BaseModel


class ProcessedDataResponse(BaseModel):
    message: str
    rows_inserted: int