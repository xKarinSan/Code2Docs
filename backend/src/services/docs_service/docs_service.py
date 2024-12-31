import json
from typing import Dict, Any, List
from datetime import datetime
from backend.src.services.db_service.models.DocModel import DocModel
from backend.src.services.db_service.models.DocSetModel import DocSetModel
from backend.src.services.db_service.models.CodebaseModel import CodebaseModel
from backend.src.services.db_service.models.DocModel import DocModel

from backend.src.services.docs_service.schemas.DocSchemas import Docs
from backend.src.services.docs_service.schemas.DocSetSchemas import DocSet
from backend.src.services.codebase_service.codebase_service import codebase_service
from backend.src.services.db_service.db import get_db


class DocsService:
    # ================ for document sets ================
    def create_new_docset(self, docset: Dict[str, str]) -> Dict[str, Any]:
        # check if user is allowed to access codebase
        db_session = next(get_db())
        authorised_codebase = codebase_service.get_codebase_by_id(
            docset["codebase_id"], docset["user_id"]
        )
        if authorised_codebase is None:
            return None

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
                .join(
                    CodebaseModel, DocSetModel.codebase_id == CodebaseModel.codebase_id
                )
                .filter(
                    CodebaseModel.user_id == user_id, DocSetModel.docset_id == docset_id
                )
                .first()
            )
            if docset is None:
                return None
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

    # ================ for documents themselves ================
    def create_new_doc(self, create_doc_dict: Dict[str, str]) -> Dict[str, Any]:
        # check if user is allowed to access docset
        db_session = next(get_db())
        authorised_docset = (
            db_session.query(DocSetModel)
            .join(CodebaseModel)
            .filter(
                CodebaseModel.user_id == create_doc_dict["user_id"],
                DocSetModel.docset_id == create_doc_dict["docset_id"],
            )
            .first()
        )
        if authorised_docset is None:
            return None
        # create the codebase
        new_doc_dict = {
            "docset_id": create_doc_dict["docset_id"],
            "date_generated": datetime.now(),
            "doc_name": create_doc_dict["doc_name"],
            "contents": create_doc_dict["contents"],
        }
        new_docset = DocModel(**new_doc_dict)
        db_session.add(new_docset)
        db_session.commit()
        db_session.refresh(new_docset)
        return json.loads(Docs(**new_docset.__dict__).model_dump_json())

    def get_docs_from_docset(self, docset_id: int, user_id: str) -> List[Docs]:
        try:
            db_session = next(get_db())
            docs_from_docsets = (
                db_session.query(DocModel)
                .join(DocSetModel, DocSetModel.docset_id == DocModel.docset_id)
                .join(
                    CodebaseModel, CodebaseModel.codebase_id == DocSetModel.codebase_id
                )
                .filter(
                    CodebaseModel.user_id == user_id,
                    DocSetModel.docset_id == docset_id,
                )
                .all()
            )
            return [
                json.loads(Docs(**doc.__dict__).model_dump_json())
                for doc in docs_from_docsets
            ]
        except:
            return []

    def get_docs_by_id(self, doc_id: int, user_id: str) -> Dict[str, Any]:
        db_session = next(get_db())
        current_doc = (
            db_session.query(DocModel)
            .join(DocSetModel, DocSetModel.docset_id == DocModel.docset_id)
            .join(CodebaseModel, DocSetModel.codebase_id == CodebaseModel.codebase_id)
            .filter(CodebaseModel.user_id == user_id, DocModel.doc_id == doc_id)
            .first()
        )
        if current_doc is None:
            return None
        return json.loads(Docs(**current_doc.__dict__).model_dump_json())

    def get_docs_by_user(self, user_id: str) -> List[Docs]:
        db_session = next(get_db())
        user_docs = (
            db_session.query(DocModel)
            .join(DocSetModel, DocSetModel.docset_id == DocModel.docset_id)
            .join(CodebaseModel, DocSetModel.codebase_id == CodebaseModel.codebase_id)
            .filter(CodebaseModel.user_id == user_id)
            .all()
        )
        return [json.loads(Docs(**doc.__dict__).model_dump_json()) for doc in user_docs]


docs_service = DocsService()
