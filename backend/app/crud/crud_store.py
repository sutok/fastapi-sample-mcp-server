from typing import List, Optional
from firebase_admin import firestore
from datetime import datetime
from ..models.store import StoreCreate, StoreUpdate, StoreInDB


class CRUDStore:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection("stores")

    async def create(self, obj_in: StoreCreate) -> StoreInDB:
        # 企業の存在確認
        company_ref = self.db.collection("companies").document(obj_in.company_id)
        company_doc = company_ref.get()
        if not company_doc.exists:
            raise ValueError("指定された企業が存在しません")

        doc_ref = self.collection.document()
        store_data = obj_in.model_dump()
        store_data.update(
            {
                "id": doc_ref.id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )
        doc_ref.set(store_data)
        return StoreInDB(**store_data)

    async def get(self, store_id: str) -> Optional[StoreInDB]:
        doc = self.collection.document(store_id).get()
        if doc.exists:
            return StoreInDB(**{**doc.to_dict(), "id": doc.id})
        return None

    async def get_multi(
        self, company_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[StoreInDB]:
        query = self.collection
        if company_id:
            query = query.where("company_id", "==", company_id)

        docs = query.limit(limit).offset(skip).stream()
        return [StoreInDB(**{**doc.to_dict(), "id": doc.id}) for doc in docs]

    async def update(self, store_id: str, obj_in: StoreUpdate) -> Optional[StoreInDB]:
        doc_ref = self.collection.document(store_id)
        if not doc_ref.get().exists:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        doc_ref.update(update_data)
        updated_doc = doc_ref.get()
        return StoreInDB(**{**updated_doc.to_dict(), "id": store_id})

    async def delete(self, store_id: str) -> bool:
        doc_ref = self.collection.document(store_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True


crud_store = CRUDStore()
