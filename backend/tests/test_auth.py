import pytest
from fastapi import status
from unittest.mock import Mock, patch
import firebase_admin.auth


@pytest.fixture
def mock_auth():
    """Firebase認証のモック"""
    mock_auth = Mock()

    # ユーザーモックの設定
    mock_user = Mock()
    mock_user.uid = "test_uid"
    mock_user.email = "test@example.com"
    mock_user.email_verified = True

    mock_auth.get_user_by_email.return_value = mock_user
    mock_auth.create_custom_token.return_value = "mocked_token"

    with patch("firebase_admin.auth", mock_auth):
        yield mock_auth


def test_login_success(client, mock_auth):
    """ログイン成功のテスト"""
    login_data = {"email": "test@example.com", "password": "testpassword"}

    # エミュレータのレスポンスをモック
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "idToken": "test_token",
        "email": "test@example.com",
        "localId": "test_uid",
        "expiresIn": "3600",
    }

    with patch("requests.post", return_value=mock_response):
        response = client.post("/api/v1/auth/login", json=login_data)
        if response.status_code != status.HTTP_200_OK:
            print_response_details(response)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, mock_auth):
    """無効な認証情報でのログイン失敗テスト"""
    login_data = {"email": "invalid@example.com", "password": "wrongpassword"}

    # エミュレータのエラーレスポンスをモック
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"error": {"message": "INVALID_PASSWORD"}}

    with patch("requests.post", return_value=mock_response):
        response = client.post("/api/v1/auth/login", json=login_data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_signup_success(client, mock_auth):
    """サインアップ成功のテスト"""
    signup_data = {
        "email": "newuser@example.com",
        "password": "newpassword",
        "username": "newuser",
    }

    # エミュレータのレスポンスをモック
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "idToken": "test_token",
        "email": signup_data["email"],
        "localId": "new_user_id",
        "expiresIn": "3600",
    }

    with patch("requests.post", return_value=mock_response):
        response = client.post("/api/v1/auth/signup", json=signup_data)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == signup_data["email"]


def print_response_details(response):
    """レスポンスの詳細を出力するヘルパー関数"""
    print("\nResponse Status:", response.status_code)
    print("Response Headers:", dict(response.headers))
    print("Response Body:", response.text)
    if response.status_code != status.HTTP_200_OK:
        print("Error Details:", response.json())
