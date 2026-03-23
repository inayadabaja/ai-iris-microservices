from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

processed_engine = create_engine(settings.processed_database_url)
ProcessedSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=processed_engine)