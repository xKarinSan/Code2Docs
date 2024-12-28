from typing import Dict, List
from backend.src.services.codebase_service.CodebaseSchemas import (
    Codebase,
)
from backend.src.services.db_service.models.CodebaseModel import CodebaseModel
from backend.src.services.db_service.db import get_db
from datetime import datetime
import json


class CodebaseService:
    # def __init__(self):
    #     self.db_session_generator = get_db()

    """
    Create codebase
    """

    def create_codebase(self, codebase: Dict[str, str]) -> Codebase | None:
        try:
            db_session = next(get_db())
            codebase["date_uploaded"] = datetime.now()
            new_codebase = CodebaseModel(**codebase)
            db_session.add(new_codebase)
            db_session.commit()
            db_session.refresh(new_codebase)
            return json.loads(Codebase(**new_codebase.__dict__).model_dump_json())

        except:
            return None

    """
    Get all codebases (testing only)
    """

    def get_all_codebases(self) -> List[Codebase]:
        try:
            db_session = next(get_db())
            all_codebases = db_session.query(CodebaseModel).all()
            return [
                json.loads(Codebase(**codebase.__dict__).model_dump_json())
                for codebase in all_codebases
            ]
        except:
            return []

    """
    Get authorised individual codebase (by ID)
    Input: user_id, codebase_id
    """

    def get_codebase_by_id(self, codebase_id: int, user_id: str) -> Codebase | None:
        try:
            db_session = next(get_db())
            authorised_codebase = (
                db_session.query(CodebaseModel)
                .filter(
                    CodebaseModel.codebase_id == codebase_id,
                    CodebaseModel.user_id == user_id,
                )
                .first()
            )
            return json.loads(Codebase(**authorised_codebase.__dict__).model_dump_json())
        except:
            return None

    """
    Get all codebases of user
    Input: user_id
    """

    def get_all_user_codebases(self, user_id: str) -> List[Codebase]:
        try:
            db_session = next(get_db())
            user_codebases = (
                db_session.query(CodebaseModel)
                .filter(CodebaseModel.user_id == user_id)
                .all()
            )
            return [
                json.loads(Codebase(**codebase.__dict__).model_dump_json())
                for codebase in user_codebases
            ]
        except:
            return []

    """
    Delete codebase
    Input: user_id, codebase_id
    """


codebase_service = CodebaseService()
