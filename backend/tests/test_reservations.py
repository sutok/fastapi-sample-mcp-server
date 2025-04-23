from datetime import datetime, timedelta, date
import pytest
from fastapi import status
from app.models.reservation import ReservationStatus


@pytest.fixture
def sample_reservation_data():
    future_date = (datetime.now() + timedelta(days=30)).date()  # 1ヶ月後の日付
    return {
        "reservation_date": future_date.isoformat(),
        "reservation_time": "15:30",
        "notes": "テスト予約",
    }


@pytest.mark.asyncio
async def test_create_reservation(client, sample_reservation_data, auth_headers):
    response = client.post(
        "/api/v1/reservations/", json=sample_reservation_data, headers=auth_headers
    )
    if response.status_code != 201:
        print("Error response:", response.json())  # エラーの詳細を出力
    assert response.status_code == 201
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
