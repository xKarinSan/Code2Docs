from backend.src.services.db_service.models.CodebaseModel import CodebaseModel
from backend.src.services.db_service.models.DocModel import DocModel
from backend.src.services.db_service.models.DocSetModel import DocSetModel
from backend.src.services.db_service.db import Base, engine


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)