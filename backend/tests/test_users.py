import pytest
from fastapi import status


def test_read_user_me(client, auth_headers, mock_firebase_auth):
    """現在のユーザー情報取得テスト"""
    response = client.get("/api/v1/users/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "test@example.com"


def test_update_user_me(client, auth_headers, mock_firebase_auth):
    """ユーザー情報更新テスト"""
    update_data = {"name": "Updated Name"}
    response = client.put("/api/v1/users/me", headers=auth_headers, json=update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Updated Name"


def test_unauthorized_access(client):
    """未認証アクセスのテスト"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
