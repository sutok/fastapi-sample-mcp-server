import pytest
from datetime import date, time
from app.models.reservation import ReservationCreate, ReservationStatus


@pytest.fixture
def sample_reservation_data():
    return {
        "reservation_date": date(2025, 4, 18),
        "reservation_time": "15:30",
        "notes": "テスト予約",
    }


@pytest.fixture
def sample_reservation_create(sample_reservation_data):
    return ReservationCreate(**sample_reservation_data)


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


# 他のテストケースも同様に修正...
