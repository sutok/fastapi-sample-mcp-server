import firebase_admin
from firebase_admin import credentials, firestore, auth
from .config import settings
import os
import logging

logger = logging.getLogger(__name__)

_firestore_client = None
_is_initialized = False


def initialize_firebase():
    """Firebase SDKの初期化"""
    global _firestore_client, _is_initialized

    if not _is_initialized:
        try:
            # 開発環境の場合、エミュレータの設定
            if settings.ENVIRONMENT == "development":
                os.environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8080"
                os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "127.0.0.1:9099"
                logger.info("Firebase Emulator settings configured")

            # 認証情報の設定
            cred = credentials.Certificate(settings.firebase_credentials)

            # Firebaseの初期化
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred, {"projectId": "demo-project"})
                logger.info("Firebase Admin SDK initialized")

            _firestore_client = firestore.client()
            _is_initialized = True
            logger.info("Firestore client initialized")

            # エミュレータ接続の確認
            if settings.ENVIRONMENT == "development":
                try:
                    # テストドキュメントの作成と削除
                    test_ref = _firestore_client.collection("_test").document()
                    test_ref.set({"test": True})
                    test_ref.delete()
                    logger.info("Successfully connected to Firestore Emulator")
                except Exception as e:
                    logger.error(f"Failed to connect to Firestore Emulator: {e}")
                    raise

        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            raise


def get_firestore():
    """初期化済みのFirestoreクライアントを取得"""
    global _firestore_client
    if not _is_initialized:
        initialize_firebase()
    return _firestore_client


def get_auth():
    """初期化済みのAuth clientを取得"""
    if not _is_initialized:
        initialize_firebase()
    return auth
