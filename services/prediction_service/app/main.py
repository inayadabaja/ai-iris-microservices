from fastapi import FastAPI
from app.api.routes import router
from app.core.config import settings
from app.core.database import app_engine
from app.models.prediction_model import Base

app = FastAPI(title=settings.APP_NAME)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=app_engine)


app.include_router(router)