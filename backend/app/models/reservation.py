from datetime import date, time, datetime, timedelta, timezone
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class ReservationStatus(str, Enum):
    """予約ステータス"""

    ACCEPTED = "accepted"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ReservationBase(BaseModel):
    """予約基本情報（リクエスト用の基本フィールド）"""

    user_id: str = Field(..., description="ユーザーID")
    company_id: str = Field(..., description="会社ID")
    branch_id: str = Field(..., description="店舗ID")
    reservation_at: datetime = Field(..., description="予約日時（Timestamp型）")
    notes: Optional[str] = Field(
        None, max_length=500, description="備考（最大500文字）"
    )

    @field_validator("reservation_at")
    @classmethod
    def validate_reservation_at(cls, v: datetime) -> datetime:
        """予約日時のバリデーション"""
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        current_time = datetime.now(timezone.utc)

        # 営業時間のチェック
        if v.hour < 10 or v.hour >= 22:
            raise ValueError("予約時間は10:00から22:00の間で指定してください")

        return v


class ReservationCreate(ReservationBase):
    """予約作成モデル（リクエスト用）"""

    pass


class ReservationUpdate(BaseModel):
    """予約更新モデル"""

    reservation_date: Optional[date] = None
    reservation_time: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[ReservationStatus] = None


class ReservationInDBBase(ReservationBase):
    """データベース保存用の基本フィールド"""

    id: str
    user_id: str
    reception_number: int = Field(description="受付番号")
    status: ReservationStatus = ReservationStatus.CONFIRMED
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ReservationInDB(ReservationInDBBase):
    """データベース内の予約モデル（内部処理用）"""

    pass


class Reservation(ReservationInDBBase):
    """APIレスポンス用予約モデル"""

    model_config = {
        "json_encoders": {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }
    }


class TimeSlot(BaseModel):
    """時間枠モデル"""

    time: str = Field(..., description="時間（例: '10:00'）")
    is_available: bool = Field(..., description="予約可能かどうか")
    remaining_capacity: int = Field(..., ge=0, description="残り定員")

    model_config = {"from_attributes": True}


class BusinessHours(BaseModel):
    """営業時間モデル"""

    morning_start: str = "10:00"
    morning_end: str = "13:00"
    afternoon_start: str = "14:00"
    afternoon_end: str = "17:00"


class ReservationSummary(BaseModel):
    """予約状況サマリーモデル"""

    current_time: datetime
    business_hours: BusinessHours
    current_number: Optional[int] = None  # 現在の呼び出し番号
    latest_reception_number: Optional[int] = None  # 最新の受付番号
    waiting_count: int = 0  # 待機人数

    model_config = {"json_encoders": {datetime: lambda v: v.isoformat()}}
