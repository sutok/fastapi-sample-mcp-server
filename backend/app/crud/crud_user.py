from typing import Optional
from firebase_admin import firestore
from datetime import datetime
from ..models.user import UserCreate, UserUpdate
from ..core.firebase import get_firestore


class CRUDUser:
    def __init__(self):
        """
        ユーザーCRUD操作用クラスの初期化
        Firestoreのクライアントを設定
        """
        self.db = get_firestore()
        self.collection = self.db.collection("users")

    async def create(self, user: UserCreate, uid: str) -> dict:
        """
        新規ユーザーを作成する

        Args:
            user (UserCreate): 作成するユーザー情報
            uid (str): FirebaseのUID

        Returns:
            dict: 作成されたユーザー情報
        """
        user_data = {
            "uid": uid,
            "email": user.email,
            "username": user.username,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        # Firestoreにユーザーデータを保存
        self.collection.document(uid).set(user_data)
        return user_data

    async def get_by_uid(self, uid: str) -> Optional[dict]:
        """
        UIDでユーザーを取得する

        Args:
            uid (str): ユーザーのUID

        Returns:
            Optional[dict]: ユーザー情報（存在しない場合はNone）
        """
        doc = self.collection.document(uid).get()
        return doc.to_dict() if doc.exists else None

    async def update(self, uid: str, user_update: UserUpdate) -> Optional[dict]:
        """
        ユーザー情報を更新する

        Args:
            uid (str): 更新対象ユーザーのUID
            user_update (UserUpdate): 更新するユーザー情報

        Returns:
            Optional[dict]: 更新されたユーザー情報
        """
        update_data = user_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()

        self.collection.document(uid).update(update_data)
        return await self.get_by_uid(uid)


# CRUDUserのインスタンスを作成
crud_user = CRUDUser()
