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


def print_response_details(response):
    """レスポンスの詳細を出力するヘルパー関数"""
    print("\nResponse Status:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Body:", response.json())


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
    update_data = {"username": "updated_username"}
    response = client.put("/api/v1/users/me", headers=auth_headers, json=update_data)

    if response.status_code != status.HTTP_200_OK:
        print_response_details(response)

    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data["username"] == "updated_username"
    assert "email" in response_data
    assert response_data["is_active"] is True


def test_unauthorized_access(client):
    """未認証アクセスのテスト"""
    response = client.get("/api/v1/users/me")
    print(f"\nResponse status: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response body: {response.json()}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "WWW-Authenticate" in response.headers
    assert response.json()["detail"] == "認証情報がありません。"


def test_invalid_token_format(client):
    """無効なトークン形式のテスト"""
    invalid_headers = {"Authorization": "invalid_token"}
    response = client.get("/api/v1/users/me", headers=invalid_headers)
    print(f"\nResponse status: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response body: {response.json()}")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "WWW-Authenticate" in response.headers
    assert response.json()["detail"] == "無効な認証スキームです。Bearer認証が必要です。"


def test_invalid_bearer_token(client):
    """無効なBearerトークンのテスト"""
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=invalid_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "WWW-Authenticate" in response.headers
    assert response.json()["detail"] == "無効なトークンです"
