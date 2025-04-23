import pytest
from fastapi.testclient import TestClient
from firebase_admin import auth
from unittest.mock import Mock, patch, AsyncMock
from app.main import app
from app.core.firebase import initialize_firebase
from app.core.security import SecurityService, firebase_auth
from fastapi.security import HTTPAuthorizationCredentials
import jwt

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
    # 認証モックの作成
    mock_auth = Mock()
    mock_auth.get_user_by_email.return_value = Mock(
        uid="test_user_id", email="test@example.com", email_verified=True
    )
    mock_auth.create_custom_token.return_value = "test_token"

    # verify_firebase_tokenのモック関数
    async def mock_verify_token(credentials: HTTPAuthorizationCredentials):
        token = credentials.credentials
        # JWTトークンをデコード
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        return {
            "uid": "test_user_id",
            "email": "test@example.com",
            "email_verified": True,
        }

    # requestsのモック
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "users": [
            {
                "localId": "test_user_id",
                "email": "test@example.com",
                "emailVerified": True,
            }
        ]
    }

    # SecurityServiceとfirebase_adminのモック
    with patch.object(
        SecurityService, "verify_firebase_token", new=mock_verify_token
    ) as mock_verify, patch(
        "firebase_admin.auth", return_value=mock_auth
    ) as mock_firebase, patch(
        "requests.post", return_value=mock_response
    ):
        mock_firebase.get_user_by_email = mock_auth.get_user_by_email
        mock_firebase.create_custom_token = mock_auth.create_custom_token
        yield mock_firebase


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
    # JWTトークンを作成
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
