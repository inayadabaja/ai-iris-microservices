from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class ProcessedIrisData(Base):
    __tablename__ = "processed_iris_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sepal_length = Column(Float, nullable=False)
    sepal_width = Column(Float, nullable=False)
    petal_length = Column(Float, nullable=False)
    petal_width = Column(Float, nullable=False)
    target = Column(Integer, nullable=False)
    dataset_type = Column(String, nullable=False)