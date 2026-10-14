from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, Integer, String

from src.database.database import Base


# Create metadata for table creation
class Todos(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)


# create pydantic model for data validation incoming database store reqs
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
