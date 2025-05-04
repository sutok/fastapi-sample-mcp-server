from typing import Optional
from firebase_admin import firestore
from datetime import datetime
from ..models.user import UserCreate, UserUpdate, User
from ..core.firebase import get_firestore
import logging

logger = logging.getLogger(__name__)


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
        try:
            current_time = datetime.utcnow()
            user_data = {
                "id": uid,  # uidをidとして使用
                "email": user.email,
                "username": user.username,
                "is_active": user.is_active,
                "role": user.role,
                "company_id": user.company_id,
                "branch_id": user.branch_id,
                "created_at": current_time,
                "updated_at": current_time,
            }

            # Firestoreにユーザーデータを保存
            doc_ref = self.collection.document(uid)
            doc_ref.set(user_data)

            return user_data
        except Exception as e:
            print(f"Error in create: {str(e)}")  # デバッグ用
            raise

    async def get_by_uid(self, uid: str) -> Optional[dict]:
        """
        UIDでユーザーを取得する

        Args:
            uid (str): ユーザーのUID

        Returns:
            Optional[dict]: ユーザー情報（存在しない場合はNone）
        """
        try:
            logger.debug(f"Fetching user with uid: {uid}")
            doc = self.collection.document(uid).get()
            if doc.exists:
                user_data = doc.to_dict()
                user_data["id"] = doc.id
                logger.debug(f"Found user data: {user_data}")
                return user_data
            logger.debug(f"No user found with uid: {uid}")
            return None
        except Exception as e:
            logger.error(f"Error in get_by_uid: {str(e)}")
            raise

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
