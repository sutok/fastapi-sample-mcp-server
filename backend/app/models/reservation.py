from datetime import date, time, datetime, timedelta
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class ReservationStatus(str, Enum):
    """予約ステータス"""

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class ReservationBase(BaseModel):
    """予約基本情報（リクエスト用の基本フィールド）"""

    user_id: str = Field(..., description="ユーザーID")
    company_id: str = Field(..., description="会社ID")
    branch_id: str = Field(..., description="店舗ID")
    reservation_date: date = Field(..., description="予約日（YYYY-MM-DD形式）")
    reservation_time: str = Field(
        ...,
        description="予約時間（HH:MM形式）",
        pattern="^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
    )
    notes: Optional[str] = Field(
        None, max_length=500, description="備考（最大500文字）"
    )

    @field_validator("reservation_date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("予約日は今日以降の日付を指定してください")
        max_date = date.today() + timedelta(days=60)
        if v > max_date:
            raise ValueError("予約は2ヶ月先までしか受け付けていません")
        return v

    @field_validator("reservation_time")
    @classmethod
    def validate_time(cls, v: str) -> str:
        try:
            # HH:MM形式の文字列をtime型に変換
            hour, minute = map(int, v.split(":"))
            reservation_time = time(hour, minute)

            # 営業時間のチェック
            if hour < 10 or hour >= 22:
                raise ValueError("予約時間は10:00から22:00の間で指定してください")

            # 30分単位のチェック
            if minute not in [0, 30]:
                raise ValueError("予約時間は30分単位で指定してください")

            return v
        except ValueError as e:
            if (
                str(e) == "予約時間は10:00から22:00の間で指定してください"
                or str(e) == "予約時間は30分単位で指定してください"
            ):
                raise
            raise ValueError("予約時間はHH:MM形式で指定してください（例: 14:30）")


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
