from typing import List, Optional
from firebase_admin import firestore
from datetime import datetime
from ..models.branch import BranchCreate, BranchUpdate, BranchInDB


class CRUDBranch:
    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection("branches")

    async def create(self, obj_in: BranchCreate) -> BranchInDB:
        # 企業の存在確認
        company_ref = self.db.collection("companies").document(obj_in.company_id)
        company_doc = company_ref.get()
        if not company_doc.exists:
            raise ValueError("指定された企業が存在しません")

        doc_ref = self.collection.document()
        branch_data = obj_in.model_dump()
        branch_data.update(
            {
                "id": doc_ref.id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        )
        doc_ref.set(branch_data)
        return BranchInDB(**branch_data)

    async def get(self, branch_id: str) -> Optional[BranchInDB]:
        doc = self.collection.document(branch_id).get()
        if doc.exists:
            return BranchInDB(**{**doc.to_dict(), "id": doc.id})
        return None

    async def get_multi(
        self, company_id: Optional[str] = None, skip: int = 0, limit: int = 100
    ) -> List[BranchInDB]:
        query = self.collection
        if company_id:
            query = query.where("company_id", "==", company_id)

        docs = query.limit(limit).offset(skip).stream()
        return [
            BranchInDB(
                **{
                    **doc.to_dict(),
                    "id": doc.id,
                    "company_id": doc.to_dict().get("company_id", "default_company_id"),
                    "branch_name": doc.to_dict().get(
                        "branch_name", "default_branch_name"
                    ),
                    "address": doc.to_dict().get("address", "default_address"),
                    "phone": doc.to_dict().get("phone", "default_phone"),
                    "business_hours": doc.to_dict().get(
                        "business_hours", "default_hours"
                    ),
                }
            )
            for doc in docs
        ]

    async def update(
        self, branch_id: str, obj_in: BranchUpdate
    ) -> Optional[BranchInDB]:
        doc_ref = self.collection.document(branch_id)
        if not doc_ref.get().exists:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        doc_ref.update(update_data)
        updated_doc = doc_ref.get()
        return BranchInDB(**{**updated_doc.to_dict(), "id": branch_id})

    async def delete(self, branch_id: str) -> bool:
        doc_ref = self.collection.document(branch_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True


crud_branch = CRUDBranch()
