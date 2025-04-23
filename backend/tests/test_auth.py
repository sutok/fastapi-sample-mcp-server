import pytest
from fastapi import status
from firebase_admin import auth
from unittest.mock import Mock, patch
import requests


def test_login_success(client, mock_firebase_auth):
    """ログイン成功のテスト"""
    # Firebase認証のモックを設定
    mock_firebase_auth.get_user_by_email.return_value.uid = "test_uid"
    mock_firebase_auth.create_custom_token.return_value = "test_token"

    # requestsのモックを設定
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "idToken": "test_token",
            "email": "test@example.com",
            "localId": "test_uid",
            "expiresIn": "3600",
        }
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com", "password": "testpassword123"},
        )
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()


def test_login_invalid_credentials(client, mock_firebase_auth):
    """無効な認証情報でのログイン失敗テスト"""
    with patch("requests.post") as mock_post:
        # エラーレスポンスをモック
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": {
                "code": 400,
                "message": "EMAIL_NOT_FOUND",
                "errors": [
                    {
                        "message": "EMAIL_NOT_FOUND",
                        "domain": "global",
                        "reason": "invalid",
                    }
                ],
            }
        }
        mock_post.return_value = mock_response

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "invalid@example.com", "password": "wrongpassword"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.json()
        assert (
            response.json()["detail"]
            == "メールアドレスまたはパスワードが正しくありません"
        )


def test_login_invalid_input(client):
    """無効な入力形式のテスト"""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "not_an_email",  # 無効なメールアドレス形式
            "password": "",  # 空のパスワード
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
