from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from backend.src.services.db_service.db import Base


class CodebaseModel(Base):
    __tablename__ = "codebase"
    codebase_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    date_uploaded = Column(DateTime)
    codebase_name = Column(String, nullable=False)
    
    docsets = relationship("DocSetModel", back_populates="codebase")
