import pytest
from fastapi.testclient import TestClient
from firebase_admin import auth
from unittest.mock import Mock, patch
from app.main import app
from app.core.firebase import initialize_firebase

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
    with patch("firebase_admin.auth") as mock_auth:
        # テスト用のユーザー情報
        mock_auth.verify_id_token.return_value = {
            "uid": "test_user_id",
            "email": "test@example.com",
            "email_verified": True,
        }
        yield mock_auth


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
    return {"Authorization": "Bearer test_token"}
