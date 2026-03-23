from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

app_engine = create_engine(settings.app_database_url)
AppSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=app_engine)