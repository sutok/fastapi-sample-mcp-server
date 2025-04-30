from datetime import date, time
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class ReservationStatus(str, Enum):
    """予約ステータス"""

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ReservationBase(BaseModel):
    """予約基本情報"""

    reservation_date: date = Field(..., description="予約日")
    reservation_time: time = Field(..., description="予約時間枠")
    notes: Optional[str] = Field(None, description="備考")


class ReservationCreate(ReservationBase):
    """予約作成スキーマ"""

    pass


class ReservationUpdate(BaseModel):
    """予約更新スキーマ"""

    date: Optional[date] = Field(None, description="予約日")
    time_slot: Optional[time] = Field(None, description="予約時間枠")
    notes: Optional[str] = Field(None, description="備考")
    status: Optional[ReservationStatus] = Field(None, description="予約ステータス")


class ReservationInDB(ReservationBase):
    """データベース内の予約スキーマ"""

    id: str = Field(..., description="予約ID")
    user_id: str = Field(..., description="予約者ID")
    status: ReservationStatus = Field(default=ReservationStatus.CONFIRMED)


class Reservation(ReservationBase):
    """APIレスポンス用予約スキーマ"""

    id: str = Field(..., description="予約ID")
    status: ReservationStatus = Field(..., description="予約ステータス")
