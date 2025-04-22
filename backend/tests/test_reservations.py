from datetime import datetime, timedelta, date
import pytest
from fastapi import status


@pytest.fixture
def sample_reservation_data():
    return {
        "reservation_date": date(2025, 4, 18),
        "reservation_time": "15:30",
        "notes": "テスト予約",
    }


async def test_create_reservation(client, sample_reservation_data, auth_headers):
    response = await client.post(
        "/api/v1/reservations/", json=sample_reservation_data, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert (
        data["reservation_date"]
        == sample_reservation_data["reservation_date"].isoformat()
    )
    assert data["reservation_time"] == sample_reservation_data["reservation_time"]
    assert data["notes"] == sample_reservation_data["notes"]
    assert "reception_number" in data
    assert data["status"] == ReservationStatus.CONFIRMED.value


def test_get_user_reservations(client, auth_headers, mock_firebase_auth):
    """ユーザーの予約一覧取得テスト"""
    response = client.get("/api/v1/reservations/", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_invalid_reservation_date(client, auth_headers, mock_firebase_auth):
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
