import json
from typing import Dict, Any
from datetime import datetime
from backend.src.services.db_service.models.DocSetModel import DocSetModel
from backend.src.services.docs_service.schemas.DocSchemas import Docs
from backend.src.services.docs_service.schemas.DocSetSchemas import DocSet
from backend.src.services.codebase_service.codebase_service import codebase_service
from backend.src.services.db_service.db import get_db


class DocsService:
    # ================ for creating document sets ================
    def create_new_document_set(self, docset: Dict[str, str]) -> Dict[str, Any]:
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

    def view_document_set_by_id(self, user_id: str, docset_id: str) -> Dict[str, Any]:
        return


docs_service = DocsService()
