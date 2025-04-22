import pytest
from fastapi import status
from firebase_admin import auth


def test_login_success(client, mock_firebase_auth):
    """ログイン成功のテスト"""
    # Firebase認証のモックを設定
    mock_firebase_auth.get_user_by_email.return_value.uid = "test_uid"
    mock_firebase_auth.create_custom_token.return_value = "test_token"

    breakpoint()
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    breakpoint()
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_login_invalid_credentials(client, mock_firebase_auth):
    """無効な認証情報でのログイン失敗テスト"""
    # Firebase認証エラーをモック
    mock_firebase_auth.get_user_by_email.side_effect = auth.AuthError(
        "INVALID_CREDENTIALS", "Invalid credentials"
    )

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "invalid@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()


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
