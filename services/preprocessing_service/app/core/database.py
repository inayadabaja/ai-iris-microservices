from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

raw_engine = create_engine(settings.raw_database_url)
processed_engine = create_engine(settings.processed_database_url)

RawSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=raw_engine)
ProcessedSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=processed_engine)