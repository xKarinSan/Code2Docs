from pydantic import BaseModel
from datetime import datetime


class _CodebaseBaseSchema(BaseModel):
    user_id: str
    codebase_name: str

    class Config:
        from_attributes = True


class Codebase(_CodebaseBaseSchema):
    codebase_id: int
    date_uploaded: datetime

    class Config:
        from_attributes = True


# for creation
class CreateCodebase(_CodebaseBaseSchema):
    class Config:
        from_attributes = True

    pass
