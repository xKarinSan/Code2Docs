from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.services.db_service.db import Base


class DocModel(Base):
    __tablename__ = "doc"
    doc_id = Column(Integer, primary_key=True, index=True)
    docset_id = Column(Integer, ForeignKey("docset.docset_id"))
    date_generated = Column(DateTime, nullable=False)
    doc_name = Column(String, nullable=False)
    contents = Column(String, nullable=False)
    
    docset = relationship("DocSetModel", back_populates="docs")
