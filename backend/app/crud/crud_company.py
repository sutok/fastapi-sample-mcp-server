from typing import List, Optional
from firebase_admin import firestore
from datetime import datetime
from ..models.company import CompanyCreate, CompanyUpdate, CompanyInDB


class CRUDCompany:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection("companies")

    async def create(self, obj_in: CompanyCreate) -> CompanyInDB:
        doc_ref = self.collection.document()
        company_data = obj_in.model_dump()
        company_data.update(
            {
                "id": doc_ref.id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )
        doc_ref.set(company_data)
        return CompanyInDB(**company_data)

    async def get(self, company_id: str) -> Optional[CompanyInDB]:
        doc = self.collection.document(company_id).get()
        if doc.exists:
            return CompanyInDB(**{**doc.to_dict(), "id": doc.id})
        return None

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[CompanyInDB]:
        docs = self.collection.limit(limit).offset(skip).stream()
        return [CompanyInDB(**{**doc.to_dict(), "id": doc.id}) for doc in docs]

    async def update(
        self, company_id: str, obj_in: CompanyUpdate
    ) -> Optional[CompanyInDB]:
        doc_ref = self.collection.document(company_id)
        if not doc_ref.get().exists:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        doc_ref.update(update_data)
        updated_doc = doc_ref.get()
        return CompanyInDB(**{**updated_doc.to_dict(), "id": company_id})

    async def delete(self, company_id: str) -> bool:
        doc_ref = self.collection.document(company_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True


crud_company = CRUDCompany()
