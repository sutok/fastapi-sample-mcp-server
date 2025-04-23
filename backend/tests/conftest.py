import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from firebase_admin import auth
from app.main import app
from app.core.firebase import initialize_firebase
from app.core.security import SecurityService
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import HTTPException, status
import jwt
from datetime import datetime
from app.core.firebase import get_firestore

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
def auth_headers():
    """認証ヘッダー"""
    return {"Authorization": "Bearer test_token"}


@pytest.fixture(autouse=True)
def cleanup_database():
    """
    テストデータベースのクリーンアップ
    各テストの前後でデータベースをクリーンアップする
    """
    db = get_firestore()

    # テスト前のクリーンアップ
    collections = ["users", "reservations"]
    for collection in collections:
        docs = db.collection(collection).stream()
        for doc in docs:
            doc.reference.delete()

    yield

    # テスト後のクリーンアップ
    for collection in collections:
        docs = db.collection(collection).stream()
        for doc in docs:
            doc.reference.delete()


@pytest.fixture
def mock_firebase_auth():
    """Firebase認証のモック"""

    async def mock_verify_token(credentials: HTTPAuthorizationCredentials):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証情報がありません",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not credentials.scheme or credentials.scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効な認証スキームです。Bearer認証が必要です。",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not credentials.credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="認証トークンがありません",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if credentials.credentials == "invalid_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="無効なトークンです",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # テストトークンの場合は有効なユーザー情報を返す
        if credentials.credentials == "test_token":
            return {
                "uid": "test_user_id",
                "email": "test@example.com",
                "email_verified": True,
            }

        # その他のトークンは無効として扱う
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="無効なトークンです",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # SecurityServiceのverify_firebase_tokenメソッドをモック化
    with patch(
        "app.core.security.SecurityService.verify_firebase_token",
        side_effect=mock_verify_token,
    ) as mock:
        yield mock


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


@pytest.fixture(autouse=True)
def setup_test_user():
    """テストユーザーのデータを作成"""
    db = get_firestore()
    users_ref = db.collection("users")

    # テストユーザーのデータを作成
    current_time = datetime.utcnow()
    test_user_data = {
        "id": "test_user_id",
        "email": "test@example.com",
        "username": "test_user",
        "is_active": True,
        "created_at": current_time,
        "updated_at": current_time,
    }

    # ドキュメントを作成
    users_ref.document("test_user_id").set(test_user_data)

    yield

    # テスト後のクリーンアップはcleanup_databaseフィクスチャで行われる


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
