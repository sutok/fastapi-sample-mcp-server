from datetime import datetime, timedelta, date
import pytest
from fastapi import status
from app.models.reservation import ReservationStatus
from app.core.firebase import get_firestore


@pytest.fixture
def sample_reservation_data():
    future_date = (datetime.now() + timedelta(days=30)).date()
    return {
        "reservation_date": future_date.isoformat(),
        "reservation_time": "14:00",  # 異なる時間枠を使用
        "notes": "テスト予約",
    }


@pytest.mark.asyncio
async def test_create_reservation(client, sample_reservation_data, auth_headers):

    db = get_firestore()
    reservations_ref = db.collection("reservations")
    # 特定の日付と時間の予約を検索
    query = reservations_ref.where(
        "reservation_date",
        "==",
        datetime.fromisoformat(sample_reservation_data["reservation_date"]),
    ).where("reservation_time", "==", sample_reservation_data["reservation_time"])
    docs = query.get()
    # 見つかった予約を削除
    for doc in docs:
        doc.reference.delete()

    # クリーンアップ後に再度予約を試行
    response = client.post(
        "/api/v1/reservations/", json=sample_reservation_data, headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["reservation_date"] == sample_reservation_data["reservation_date"]
    assert data["reservation_time"] == sample_reservation_data["reservation_time"]
    assert data["notes"] == sample_reservation_data["notes"]
    assert "reception_number" in data
    assert data["status"] == ReservationStatus.CONFIRMED.value


@pytest.mark.asyncio
async def test_get_user_reservations(client, auth_headers, mock_firebase_auth):
    """ユーザーの予約一覧取得テスト"""
    response = client.get("/api/v1/reservations/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_invalid_reservation_date(client, auth_headers, mock_firebase_auth):
    """無効な予約日のテスト"""
    reservation_data = {
        "reservation_date": (datetime.now() - timedelta(days=1)).date().isoformat(),
        "reservation_time": "14:00:00",
        "number_of_people": 2,
    }
    response = client.post(
        "/api/v1/reservations/", headers=auth_headers, json=reservation_data
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_duplicate_reservation(client, sample_reservation_data, auth_headers):
    """同じ時間枠での重複予約をテスト"""
    # 最初の予約を作成
    response1 = client.post(
        "/api/v1/reservations/", json=sample_reservation_data, headers=auth_headers
    )
    assert response1.status_code == 201

    # 同じ時間枠で2回目の予約を試みる
    response2 = client.post(
        "/api/v1/reservations/", json=sample_reservation_data, headers=auth_headers
    )
    assert response2.status_code == 409
    error_detail = response2.json()
    assert "message" in error_detail
    assert "指定された時間枠は既に予約されています" in error_detail["message"]
