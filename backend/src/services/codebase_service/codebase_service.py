from typing import Dict, List
from backend.src.services.codebase_service.CodebaseSchemas import (
    Codebase,
)
from backend.src.services.db_service.models.CodebaseModel import CodebaseModel
from backend.src.services.db_service.db import get_db_session
from datetime import datetime
import json


class CodebaseService:
    """
    Create codebase
    """

    def create_codebase(self, codebase: Dict[str, str]) -> Codebase | None:
        try:
            with get_db_session() as db_session:
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
            with get_db_session() as db_session:
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
            with get_db_session() as db_session:
                authorised_codebase = (
                    db_session.query(CodebaseModel)
                    .filter(
                        CodebaseModel.codebase_id == codebase_id,
                        CodebaseModel.user_id == user_id,
                    )
                    .first()
                )
                return json.loads(
                    Codebase(**authorised_codebase.__dict__).model_dump_json()
                )
        except:
            return None

    """
    Get all codebases of user
    Input: user_id
    """

    def get_all_user_codebases(self, user_id: str) -> List[Codebase]:
        try:
            with get_db_session() as db_session:
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
