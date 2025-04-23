import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from firebase_admin import auth
from app.main import app
from app.core.firebase import initialize_firebase
from app.core.security import SecurityService
from fastapi.security import HTTPAuthorizationCredentials
import jwt
from fastapi import HTTPException, status

# Firebaseエミュレータの設定
import os

os.environ["FIRESTORE_EMULATOR_HOST"] = "localhost:8080"
os.environ["FIREBASE_AUTH_EMULATOR_HOST"] = "localhost:9099"


@pytest.fixture(scope="session", autouse=True)
def setup_firebase():
    """テスト用のFirebase初期化"""
    initialize_firebase()


@pytest.fixture
def client():
    """テスト用のAPIクライアント"""
    return TestClient(app)


@pytest.fixture
def mock_firebase_auth():
    """Firebase認証のモック"""

    async def mock_verify_token(credentials: HTTPAuthorizationCredentials):
        if not credentials or not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="認証情報がありません"
            )

        if credentials.credentials == "invalid_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="無効なトークンです"
            )

        return {
            "uid": "test_user_id",
            "email": "test@example.com",
            "email_verified": True,
        }

    # パッチを適用
    patcher = patch.object(
        SecurityService, "verify_firebase_token", new=mock_verify_token
    )
    patcher.start()
    yield
    patcher.stop()


@pytest.fixture
def mock_requests():
    """requestsのモック"""
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "idToken": "test_token",
            "email": "test@example.com",
            "localId": "test_user_id",
            "expiresIn": "3600",
        }
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def auth_headers():
    """認証ヘッダーの作成"""
    token = jwt.encode(
        {
            "user_id": "test_user_id",
            "email": "test@example.com",
            "email_verified": True,
        },
        "secret",
        algorithm="HS256",
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(autouse=True)
async def cleanup_database():
    """各テストケース実行前にデータベースをクリーンアップ"""
    db = get_firestore()

    # クリーンアップ対象のコレクション
    collections = ["reservations", "users"]

    # テスト前のクリーンアップ
    for collection_name in collections:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.get()
        for doc in docs:
            doc.reference.delete()

    yield

    # テスト後のクリーンアップ
    for collection_name in collections:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.get()
        for doc in docs:
            doc.reference.delete()
