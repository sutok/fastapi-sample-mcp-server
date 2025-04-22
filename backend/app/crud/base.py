from typing import Any, Dict, Generic, Optional, Type, TypeVar
from firebase_admin import firestore

ModelType = TypeVar("ModelType")

class CRUDBase(Generic[ModelType]):
    def __init__(self, collection_name: str):
        self.db = firestore.client()
        self.collection = self.db.collection(collection_name)

    async def get(self, id: str) -> Optional[ModelType]:
        doc = self.collection.document(id).get()
        return doc.to_dict() if doc.exists else None

    async def create(self, obj_in: Dict[str, Any]) -> ModelType:
        doc_ref = self.collection.document()
        doc_ref.set(obj_in)
        return {**obj_in, "id": doc_ref.id}

    async def update(self, id: str, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        doc_ref = self.collection.document(id)
        if doc_ref.get().exists:
            doc_ref.update(obj_in)
            return await self.get(id)
        return None

    async def delete(self, id: str) -> bool:
        doc_ref = self.collection.document(id)
        if doc_ref.get().exists:
            doc_ref.delete()
            return True
        return False