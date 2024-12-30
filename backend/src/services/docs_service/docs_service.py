import json
from typing import Dict, Any, List
from datetime import datetime
from backend.src.services.db_service.models.DocSetModel import DocSetModel
from backend.src.services.db_service.models.CodebaseModel import CodebaseModel

from backend.src.services.docs_service.schemas.DocSchemas import Docs
from backend.src.services.docs_service.schemas.DocSetSchemas import DocSet
from backend.src.services.codebase_service.codebase_service import codebase_service
from backend.src.services.db_service.db import get_db


class DocsService:
    # ================ for creating document sets ================
    def create_new_docset(self, docset: Dict[str, str]) -> Dict[str, Any]:
        # check if user is allowed to access codebase
        db_session = next(get_db())
        authorised_codebase = codebase_service.get_codebase_by_id(
            docset["codebase_id"], docset["user_id"]
        )
        if authorised_codebase is None:
            return
        # create the codebase
        new_docset_dict = {
            "codebase_id": docset["codebase_id"],
            "date_generated": datetime.now(),
            "docset_name": docset["docset_name"],
        }
        new_docset = DocSetModel(**new_docset_dict)
        db_session.add(new_docset)
        db_session.commit()
        db_session.refresh(new_docset)
        return json.loads(DocSet(**new_docset.__dict__).model_dump_json())

    def get_docset_by_id(self, docset_id: int, user_id: str) -> Dict[str, Any]:
        try:
            db_session = next(get_db())
            docset = (
                db_session.query(DocSetModel)
                .join(CodebaseModel)
                .filter(
                    CodebaseModel.user_id == user_id, DocSetModel.docset_id == docset_id
                )
                .first()
            )
            return json.loads(DocSet(**docset.__dict__).model_dump_json())
        except:
            return None

    def get_docsets_in_codebase(self, codebase_id: int, user_id: str) -> List[DocSet]:
        try:
            db_session = next(get_db())
            user_docsets = (
                db_session.query(DocSetModel)
                .join(CodebaseModel)
                .filter(
                    CodebaseModel.user_id == user_id,
                    CodebaseModel.codebase_id == codebase_id,
                )
                .all()
            )
            return [
                json.loads(DocSet(**docset.__dict__).model_dump_json())
                for docset in user_docsets
            ]
        except:
            return []


docs_service = DocsService()
