from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.core.database import processed_engine
from app.models.processed_data_model import Base

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=processed_engine)


app.include_router(router)