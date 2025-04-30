from datetime import date, time, datetime, timedelta
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Annotated


class CompanyStatus(str, Enum):
    """予約ステータス"""

    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class CompanyBase(BaseModel):
    """予約基本情報（リクエスト用の基本フィールド）"""

    company_name: str = Field(..., description="企業名")
    address: str = Field(..., description="住所")
    phone: str = Field(..., description="電話番号")
    email: Optional[str] = Field(None, description="メールアドレス")
    notes: Optional[str] = Field(
        None, max_length=500, description="備考（最大500文字）"
    )

    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        if v == "":
            raise ValueError("企業名は必須です")
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        if v == "":
            raise ValueError("住所は必須です")
        return v


class CompanyCreate(CompanyBase):
    """予約作成モデル（リクエスト用）"""

    pass


class CompanyUpdate(BaseModel):
    """予約更新モデル"""

    company_name: Optional[str] = Field(None, description="企業名")
    address: Optional[str] = Field(None, description="住所")
    phone: Optional[str] = Field(None, description="電話番号")
    email: Optional[str] = Field(None, description="メールアドレス")
    notes: Optional[str] = Field(
        None, max_length=500, description="備考（最大500文字）"
    )
    status: Optional[CompanyStatus] = Field(None, description="ステータス")
    notes: Optional[str] = None
    status: Optional[CompanyStatus] = None


class CompanyInDBBase(CompanyBase):
    """データベース保存用の基本フィールド"""

    id: str
    company_name: str
    address: str
    phone: str
    email: Optional[str] = None
    notes: Optional[str] = None
    status: CompanyStatus = CompanyStatus.CONFIRMED
    # created_at: datetime = Field(default_factory=datetime.utcnow)
    # updated_at: datetime = Field(default_factory=datetime.utcnow)


class CompanyInDB(CompanyInDBBase):
    """データベース内の予約モデル（内部処理用）"""

    pass


class Company(CompanyInDBBase):
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
