from pydantic import BaseModel


class RawDataResponse(BaseModel):
    message: str
    rows_inserted: int