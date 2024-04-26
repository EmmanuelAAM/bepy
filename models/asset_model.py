from .base import Base
from sqlalchemy import Column, Integer, String

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
