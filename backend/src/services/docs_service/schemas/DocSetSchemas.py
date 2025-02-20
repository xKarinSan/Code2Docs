from pydantic import BaseModel
from datetime import datetime


class _DocSetBaseSchema(BaseModel):
    codebase_id: int
    docset_name: str

    class Config:
        from_attributes = True


class DocSet(_DocSetBaseSchema):
    docset_id: int
    date_generated: datetime

    class Config:
        from_attributes = True


# for creation
class CreateDocSet(_DocSetBaseSchema):
    user_id: str

    class Config:
        from_attributes = True


# for querying
class _DocSetQuery(BaseModel):
    user_id: str

    class Config:
        from_attributes = True


class DocSetQueryById(_DocSetQuery):
    docset_id: int

    class Config:
        from_attributes = True
