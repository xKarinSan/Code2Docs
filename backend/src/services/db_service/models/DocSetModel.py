from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.src.services.db_service.db import Base


class DocSetModel(Base):
    __tablename__ = "docset"
    docset_id = Column(Integer, primary_key=True, index=True)
    codebase_id = Column(Integer, ForeignKey("codebase.codebase_id"))
    date_generated = Column(DateTime, nullable=False)
    docset_name = Column(String, nullable=False)
    
    codebase = relationship("CodebaseModel", back_populates="docsets")
    docs = relationship("DocModel", back_populates="docset")
