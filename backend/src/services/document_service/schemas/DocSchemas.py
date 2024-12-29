from pydantic import BaseModel
from datetime import datetime


class _DocBaseSchema(BaseModel):
    docset_id: int
    doc_name: str
    contents: str

    class Config:
        from_attributes = True


class DocSet(_DocBaseSchema):
    doc_id: int
    date_generated: datetime

    class Config:
        from_attributes = True


# for creation
class CreateDocSet(_DocBaseSchema):
    class Config:
        from_attributes = True

    pass
