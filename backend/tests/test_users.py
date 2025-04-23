import pytest
from fastapi import status
from app.core.firebase import get_firestore
from datetime import datetime
from app.models.user import UserCreate


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

    # テスト後にユーザーを削除（クリーンアップは cleanup_database フィクスチャで行われる）


def test_read_user_me(client, auth_headers, mock_firebase_auth):
    """現在のユーザー情報取得テスト"""
    print("Auth headers:", auth_headers)  # 認証ヘッダーの内容を確認

    response = client.get("/api/v1/users/me", headers=auth_headers)
    if response.status_code != status.HTTP_200_OK:
        print("Error response:", response.json())
        print("Response headers:", response.headers)  # レスポンスヘッダーも確認

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    print("Response data:", data)
    assert data["email"] == "test@example.com"
    assert data["id"] == "test_user_id"


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
